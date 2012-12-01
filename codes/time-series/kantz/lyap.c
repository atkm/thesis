#define IFUM 200

void lyap(long nmax, float *y, long id,  long m, float eps,
  long ifu, float *s, long nmin, long nfmin, long ncmin)
{
  long i,nc,nf,np,n,nn,nfound;
  static long jh[IM*IM+1],jpntr[NX],nlist[NX];
  static float sh[IFUM];

  if(nmax>NX || ifu>IFUM) {printf("Make NX/IFUM larger."); exit(1);}
  base(nmax-ifu,y,id,m,jh,jpntr,eps);
  for(i=0; i<ifu; i++) s[i]=0;
  for(nc=0, n=(m-1)*id; n<nmax-ifu && nc<ncmin; n++){  
    for(i=0; i<ifu; i++) sh[i]=0;                        /* reference points */
    nfound=neigh(nmax-ifu,y,n,nmax,id,m,jh,jpntr,eps,nlist);
    for(nf=0, nn=0; nn<nfound; nn++){
      np=nlist[nn];
      if(abs(n-np)>nmin){
        nf++;                                           /* average distances */
        for(i=0; i<ifu; i++) sh[i]+=fabs((double)(y[n+i]-y[np+i]));
      }        
    }                      
    if(nf>=nfmin){                    /* enough neighbours closer $\epsilon$ */
      nc++;                             /* average log of averaged distances */
      for(i=0; i<ifu; i++) s[i]+=LOG(sh[i]/nf);
    }
  }
/*!*/ printf("tried %d reference points, nc=%d\n",n,nc);
  if(nc) for(i=0; i<ifu; i++) s[i]=s[i]/nc; 
}
