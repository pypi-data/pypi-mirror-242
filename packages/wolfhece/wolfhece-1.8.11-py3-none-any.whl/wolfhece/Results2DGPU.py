import numpy as np
import numpy.ma as ma
from os import path
from pathlib import Path
from scipy.sparse import csr_array
from multiprocessing import Pool
from typing import Union
from tqdm import tqdm

from .PyTranslate import _
from .wolf_array import WolfArray
from .wolfresults_2D import Wolfresults_2D, views_2D, getkeyblock
from .CpGrid import CpGrid
from .PyPalette import wolfpalette
from .gpu.results_store import ResultsStore

class wolfres2DGPU(Wolfresults_2D):
    """
    Gestion des résultats du code GPU 2D
    Surcharge de "Wolfresults_2D"
    """

    def __init__(self,
                 fname:str,
                 eps=0.,
                 idx: str = '',
                 plotted: bool = True,
                 mapviewer=None,
                 store = None):

        super().__init__(fname = str(Path(fname).parent / "simul"), eps=eps, idx=idx, plotted=plotted, mapviewer=mapviewer, gpu_loader=True)

        # MERGE Inheriting is a bad idea in general because it allows
        # classes to look inside others, and induces hard
        # coupling. It's better to connect with instances and use
        # their functions so that the provider can better enforce what
        # is available to class's users.

        if store is None:
            self._result_store = ResultsStore(sim_path = Path(fname), mode='r')
        else:
            self._result_store = store

    def get_nbresults(self):
        """
        Récupération du nombre de résultats

        Lecture du fichier de tracking afin de permettre une mise à jour en cours de calcul
        """
        self._result_store._read_track_files()
        return self._result_store.nb_results

    def read_oneresult(self, which:int=-1):
        """
        Lecture d'un pas de sauvegarde

        which: result number to read; 0-based; -1 == last one
        """
        which = self._result_store.nb_results-1 if which==-1 else which

        _, _, _, _, wd_np, qx_np, qy_np = self._result_store.get_result(which+1)

        curblock = self.myblocks[getkeyblock(1,False)]
        if self.epsilon > 0.:
            curblock.waterdepth.array=ma.masked_less_equal(wd_np.astype(np.float32).T,self.epsilon)
        else:
            curblock.waterdepth.array=ma.masked_equal(wd_np.astype(np.float32).T,0.)

        curblock.qx.array=ma.masked_where(curblock.waterdepth.array.mask,qx_np.astype(np.float32).T)
        curblock.qy.array=ma.masked_where(curblock.waterdepth.array.mask,qy_np.astype(np.float32).T)

        curblock.waterdepth.count()
        curblock.qx.count()
        curblock.qy.count()

        if self.epsilon > 0.:
            curblock.waterdepth.set_nullvalue_in_mask()
            curblock.qx.set_nullvalue_in_mask()
            curblock.qy.set_nullvalue_in_mask()

        self.current_result = which
        self.loaded=True

    def _update_result_view(self):
        """
        Procédure interne de mise à jour du pas

        Etapes partagées par read_next et read_previous
        """
        which = self.current_result

        self.read_oneresult(which)

        self.current_result = which
        self.loaded=True

    def read_next(self):
        """
        Lecture du pas suivant
        """
        self.current_result+=1

        self._update_result_view()

    def get_times_steps(self):
        """
        Récupération des temps réels et les pas de calcul de chaque résultat sur disque
        """
        return self._result_store.times_steps

    def read_previous(self):
        """
        Lecture du pas suivant
        """
        self.current_result -= 1

        self._update_result_view()

def _load_res(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    _, _, _, _, wd_np, qx_np, qy_np = store.get_result(i+1)
    return csr_array(wd_np), csr_array(qx_np), csr_array(qy_np)

def _load_res_h(x) -> tuple[csr_array, csr_array, csr_array]:
    store:ResultsStore
    i:int

    store, i = x
    wd_np = store.get_result_h(i+1)
    return csr_array(wd_np)

class Results2DGPU():
    """
    Gestion en mémoire de plusieurs résultats GPU
    Stockage CSR afin d'économiser la mémoire (Scipy CSR)
    """

    def __init__(self, fname:str, start_idx:int, end_idx:int, only_h=False) -> None:
        """
        Chargement de résultats sur base du répertoire de sauvegarde de la simulation GPU

        Lecture des résultats depuis start_idx jusque end_idx

        only_h force la lecture de la hauteur d'eau seulement, sinon (h,qx,qy)
        """

        self._results:Union[list[tuple[csr_array, csr_array, csr_array]], list[csr_array]] # typage

        # ResultsStore unique
        self._result_store = ResultsStore(Path(fname), mode='r')
        self._only_h = only_h

        if end_idx>start_idx:
            start_idx = max(start_idx,0)
            end_idx   = min(end_idx+1, self._result_store.nb_results)

            # Lecture en multiprocess des résultats
            if only_h:
                with Pool() as pool:
                    self._results = pool.map(_load_res_h, [(self._result_store,i) for i in range(start_idx, end_idx)])
            else:
                with Pool() as pool:
                    self._results = pool.map(_load_res, [(self._result_store,i) for i in range(start_idx, end_idx)])

    @property
    def only_h(self):
        return self._only_h

    def __getitem__(self,i:int):
        """Surcharge de l'opérateur []"""
        return self._results[i]

    def get_h(self, idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de hauteur d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """
        if not self.only_h:
            return self._results[idx][0].toarray() if dense else self._results[idx][0]
        else:
            return self._results[idx].toarray() if dense else self._results[idx]

    def get_qx(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit X d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][1].toarray() if dense else self._results[idx][1]
        else:
            return None

    def get_qy(self,idx:int, dense:bool=True) -> Union[np.ndarray, csr_array]:
        """
        Retourne la matrice de débit Y d'eau de la position idx (0-based)
            - en CSR (Scipy CSR)
            - en dense (Numpy array)
        """

        if not self.only_h:
            return self._results[idx][2].toarray() if dense else self._results[idx][2]
        else:
            return None

    def danger_map(self, start:int=0, end:int=-1, every:int=1) -> Union[WolfArray, tuple[WolfArray, WolfArray, WolfArray]]:
        """
        Create Danger Maps

        From start to end (index 0-based)
        Indexes are related to the self._results, not the absolute GPU results
        """

        # If __init__ with only_h==True, only wd is pre-loaded into memory
        # all_maps ==True is more than one Numpy array in self.results
        all_maps = not self.only_h

        # Number of  time steps
        number_of_time_steps = len(self._results)
        if end ==-1:
            end = number_of_time_steps

        # Init Danger Maps based on results type
        # GPU --> 1 block, Numpy array
        danger_map_matrix_h = self.get_h(0, dense=True)

        # set zeros
        danger_map_matrix_h[:,:] = 0.

        if all_maps:
            danger_map_matrix_v   = danger_map_matrix_h.copy()
            danger_map_matrix_mom = danger_map_matrix_h.copy()
            danger = [danger_map_matrix_h, danger_map_matrix_v, danger_map_matrix_mom]

        if all_maps:

            for time_step in tqdm(range(start, end, every)):

                wd = self.get_h(time_step, dense=True)
                qx = self.get_qx(time_step, dense=True)
                qy = self.get_qy(time_step, dense=True)

                v = np.zeros(wd.shape)
                mom = np.zeros(wd.shape)

                i,j = np.where(wd > 0.)
                v[i,j] = (qx[i,j]**2.+qy[i,j]**2.)**.5/wd[i,j]

                mom = v*wd

                comp = [wd, v, mom]

                # Comparison
                for curdanger, curcomp in zip(danger, comp):
                    i,j = np.where(curdanger < curcomp)
                    curdanger[i,j] = curcomp[i,j]

        else:
            for time_step in tqdm(range(start, end, every)):

                wd = self.get_h(time_step)
                i,j = np.where(danger_map_matrix_h < wd)
                danger_map_matrix_h[i,j] = wd[i,j]


        if all_maps:
            return (danger_map_matrix_h, danger_map_matrix_v, danger_map_matrix_mom)
        else:
            return danger_map_matrix_h
