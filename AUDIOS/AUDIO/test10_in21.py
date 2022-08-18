import swifter
import time
import glob, pandas as pd
from audio import *

df=pd.DataFrame(dict(file=glob.glob('*.wav')))
df=df.head(10)

t0=time.time()
df['JS']=df.file.swifter.apply(lambda fn: JitterShimmer(fn, False))
print('DT10=',round(time.time()-t0,2))
