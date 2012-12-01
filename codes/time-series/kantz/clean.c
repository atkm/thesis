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
