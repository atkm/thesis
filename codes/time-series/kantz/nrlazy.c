void nrlazy(long nmax, float *y, float *yc, long m, float eps)
{
  static long i,n,nn,nfound,jh[IM*IM+1],jpntr[NX],nlist[NX];
  float av;

  if(nmax>NX) {printf("Make NX larger."); exit(1);}
  base(nmax,y,1,m,jh,jpntr,eps);
  for(n=0; n<nmax; n++) yc[n]=y[n];
  for(n=m-1; n<nmax; n++){ 
    nfound=neigh(nmax,y,n,nmax,1,m,jh,jpntr,eps,nlist);
    for(nn=0, av=0; nn<nfound; nn++) av+=y[nlist[nn]-(m-1)/2];
    yc[n-(m-1)/2]=av/nfound;                    /* average middle coordinate */
  }
}
