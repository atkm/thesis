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
