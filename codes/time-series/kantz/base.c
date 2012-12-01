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
