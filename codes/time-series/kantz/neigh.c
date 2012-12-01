long neigh(long nmax, float *y, long n, long nlast, long id, 
  long m, long *jh, long *jpntr, float eps, long *nlist)
{
  long jj,kk,i,j,k,jk,ip,np,nfound;

  jj=y[n]/eps; 
  kk=y[n-(m-1)*id]/eps;
  for(nfound=0, j=jj-1; j<=jj+1; j++){            /* scan neighbouring boxes */
    for(k=kk-1; k<=kk+1; k++){
      jk=INDEX(j,k); 
      for(ip=jh[jk+1]; ip>jh[jk]; ip--){            /* this is in time order */
        np=jpntr[ip];
        if(np>=nlast) break;
        for(i=0; i<m; i++)
          if(fabs((double)(y[n-i*id]-y[np-i*id]))>=eps) break;
        if(i==m) nlist[nfound++]=np;              /* make list of neighbours */
      }
    }
  }
  return nfound;
}
