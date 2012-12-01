void correl(long nmax, float *y, float eps, long m, float *c, 
  long id, long nmin, long ncmin, long ipmin)
{
  long i,nn,np,n,nlast,nfound;
  static long jh[IM*IM+1],ipairs[MM],jpntr[NX],nlist[NX];
  float s;

  if(nmax>NX || m>MM) {printf("Make NX/MM larger."); exit(1);}
  for(i=1; i<m; i++) ipairs[i]=0;
  base(nmax,y,id,2,jh,jpntr,eps);
  for(n=(m-1)*id; n<nmax; n++){ 
    nfound=neigh(nmax,y,n,n-nmin,id,2,jh,jpntr,eps,nlist);
    ipairs[1]+=nfound;                   /* all neighbours in two dimensions */
    for(nn=0; nn<nfound; nn++){
      np=nlist[nn];
      if(np>=(m-1)*id)
        for(i=2; i<m; i++){
          if(fabs((double)(y[n-i*id]-y[np-i*id]))>=eps) break;
          ipairs[i]++;              /* neighbours in $3,\ldots,m$ dimensions */
        }
    }
    if(n-nmin-(m-1)*id >= ncmin && ipairs[m-1] >= ipmin) break;
  }
  s=(float)(n-nmin-(m-1)*id+1)*(float)(n-nmin-(m-1)*id)/2;
  for(i=1; i<m; i++) c[i+1]=ipairs[i]/s;                    /* normalisation */
/*!*/   printf("%f %ld %f %ld %ld\n", eps, n-(m-1)*id,s,ipairs[2],ipairs[m-1]);
}
