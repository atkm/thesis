float fclazy(long nmax, float *y, long m, float *s, long id, 
  long ifo, float eps)
{
  float av;
  long n,nfound,i;

  for(av=0, nfound=0; nfound==0; eps*=1.2){
    for(n=(m-1)*id; n<nmax-ifo; n++){ 
      for(i=0; i<m; i++)
        if(fabs((double)(y[n-(m-(i+1))*id]-s[i]))>=eps) break; 
      if(m==i){                                    /* if got here: neighbour */
        nfound++;
        av+=y[n+ifo];                   /* average over future of neighbours */
      }      
    } 
  }
  return av/nfound;
}
