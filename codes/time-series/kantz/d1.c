void d1(long nmax, float *y, long m, long id, long ncmin, float *pln, 
  float *eln, float eps0, long nmin, long kmax)
{
  long i,iu,iunp,nn,np,ip,n,nfound,nf,ncomp,k,nmd;
  static long jh[IM*IM+1],jpntr[NX],ju[NX],nlist[NX];
  static float eps,dis,e,d[NX];

  if(nmax>NX) {printf("Make NX larger."); exit(1);}
  ncomp=nmax;
  k=(long) (exp(*pln)*(nmax-2*nmin-1))+1;
  if(k>kmax){
    ncomp=(float)(nmax-2*nmin-1)*(float)kmax/(float)k+2*nmin+1;
    k=kmax;
  }
  *pln=psi(k)-log((double)(ncomp-2*nmin+1));
/*!*/  printf("Mass %f. k=%ld n=%ld\n", exp(*pln),k,ncomp);
  iu=ncmin-(m-1)*id;
  for(i=0; i<iu; i++) ju[i]=i+(m-1)*id;
  for(*eln=0, eps=eps0; iu; eps*=sqrt(2.)){
    base(ncomp,y,id,m,jh,jpntr,eps);
    for(iunp=0, nn=0; nn<iu; nn++){
      n=ju[nn];
      nfound=neigh(nmax,y,n,nmax,id,m,jh,jpntr,eps,nlist);
      for(nf=0, ip=0; ip<nfound; ip++){
        np=nlist[ip];
        nmd=abs(np-n)%ncomp;
        if(nmd<=nmin || nmd >= ncomp-nmin) continue;
        for(dis=0, i=0; i<m*id; i+=id) 
          dis=MAX(dis,fabs(y[n-i]-y[np-i]));
        d[nf++]=dis;
      }
      if(nf<k)                                /* not enough neighbours found */
        ju[iunp++]=n;                                 /* mark for next sweep */
      else{
        e=which(k,nf,d);
        *eln+=LOG(e);
      }
    }
    iu=iunp;
  }
  *eln/=(float)(ncmin-(m-1)*id);
}
