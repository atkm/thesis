#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#define NX 50000
#define MM 15
#define MAX(a,b) (a)>(b) ? (a) : (b)
#define MIN(a,b) (a)<(b) ? (a) : (b)
#define LOG(a) (((a)>1e-20)? log((a)): log(1e-20))

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

#define IM         100
#define II         100000000
#define INDEX(a,b) (IM*(((long)(a)+II)%IM) + ((long)(b)+II)%IM)

void base(long nmax, float *y, long id, long m, long *jh, 
  long *jpntr, float eps)
{
  long i,n;

  for(i=0; i<IM*IM+1; i++) jh[i]=0;
  for(n=(m-1)*id; n<nmax; n++) 
    jh[ INDEX(y[n]/eps, y[n-(m-1)*id]/eps) ]++;  
  for(i=1; i<IM*IM+1; i++) jh[i]+=jh[i-1];           /* accumulate histogram */
  for(n=(m-1)*id; n<nmax; n++){                  /* fill list of ``pointers" */
    i=INDEX(y[n]/eps, y[n-(m-1)*id]/eps);
    jpntr[jh[i]--]=n;
  }
}

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

#define MFRAC 20
#define MEPS 1000

void stplot(long nmax, float *y, long m, long id, float epsmax, 
  float stp[][MFRAC], long idt, long mdt)
{
  static long ihist[MEPS],it,ieps,n,ifrac,need,is,i;
  static float dis;

  for(it=0; it<mdt; it++){
    for(ieps=0; ieps<MEPS; ieps++) ihist[ieps]=0;
    for(n=it*idt+(m-1)*id; n<nmax; n++){
      for(dis=0, i=0; i<m; i++)   /* distance in $m$ dimensions */
        dis=MAX(dis, fabs(y[n-i*id]-y[n-i*id-it*idt]));
      ihist[ MIN( ((long)(MEPS*dis/epsmax)), MEPS-1) ]++;
    }
    for(ifrac=0; ifrac<MFRAC; ifrac++){
      need=(nmax-it*idt-(m-1)*id)*(ifrac+1)/(float)MFRAC;
      for(is=0, ieps=0; ieps<MEPS && is<need; ieps++) 
        is+=ihist[ieps];
      stp[it][ifrac]=ieps*(epsmax/MEPS);
    }
  }
}

#define SMALL 0.0001

void clean(long nmax, float *y, float *yc, long m, long kmin, 
  long nq, float d)
{
  long i,j,istep,np,n,nn,nfound,iq,iu,iunp;
  static long jh[IM*IM+1],jpntr[NX],ju[NX],nlist[NX];
  static float s,eps,r[MM],c[MM][MM],cm[MM];
  static float zcm[NX][MM];                                           /* \TR */

  if(nmax>NX || m>MM) {printf("Make NX/MM larger."); exit(1);}
  for(i=0; i<m; i++)                                    /* ${\rm tr}(1/r)=1$ */
    r[i]= (i==0 || i==m-1)? (2*SMALL+m-2)/SMALL: 2*SMALL+m-2;
  for(i=0; i<nmax; i++) yc[i]=y[i];
  for(istep=1; istep<=2; istep++){                                    /* \TR */
    iu=nmax-m+1;
    for(i=0; i<iu; i++) ju[i]=i+m-1;
    for(eps=d; iu; eps*=sqrt(2.)){
      base(nmax,y,1,m,jh,jpntr,eps);
      for(iunp=0, nn=0; nn<iu; nn++){
        n=ju[nn];
        nfound=neigh(nmax,y,n,nmax,1,m,jh,jpntr,eps,nlist);
        if(nfound<kmin)                       /* not enough neighbours found */
          ju[iunp++]=n;                               /* mark for next sweep */
        else{                                     /* enough neighbours found */
          for(i=0; i<m; i++){                      /* centre of mass vector: */
            for(s=0, np=0; np<nfound; np++) s+=y[nlist[np]-m+i+1];
            cm[i]=s/nfound; 
          }
          if(istep==1)                                                /* \TR */
            for(i=0; i<m; i++) zcm[n][i]=cm[i];       /* store cm vector \TR */
          else{                                                       /* \TR */
            for(i=0; i<m; i++){                   /* corrected cm vector \TR */
              for(s=0, np=0; np<nfound; np++)                         /* \TR */
                s+=zcm[nlist[np]][i];                                 /* \TR */
              cm[i]=2*cm[i]-s/nfound;                                 /* \TR */
            }                                                         /* \TR */
            for(i=0; i<m; i++)                              /* do projection */
              for(j=i; j<m; j++){              /*  compute covariance matrix */
                for(s=0, np=0; np<nfound; np++)
                  s+=(y[nlist[np]-m+i+1]-cm[i])
                    *(y[nlist[np]-m+j+1]-cm[j]);
                c[j][i]=c[i][j]=r[i]*r[j]*s/nfound;
              }                  
            eigen(c,m);                     /* find eigenvectors (increasing)*/
            for(i=0; i<m; i++){
              for(s=0, iq=0; iq<nq; iq++)
                for(j=0; j<m; j++) 
                  s+=(y[n-m+j+1]-cm[j])*c[i][iq]*c[j][iq]*r[j];
              yc[n-m+i+1]-=s/r[i]/r[i];
            }
          }                                                           /* \TR */
        }
      }
      iu=iunp;
/*!*/   printf("#With %f: %d uncorrected\n", eps, iu);
    }
  }                                        /* ends loop over {\tt istep} \TR */
}

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
