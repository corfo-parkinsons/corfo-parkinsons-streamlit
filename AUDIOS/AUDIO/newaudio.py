import glob, time
import pandas as pd

import parselmouth
from parselmouth.praat import call

import statistics
from ppe import PPE
###############

F0min, F0max = 75, 500
voicerep = lambda spp: call(spp, "Voice report", 0.0, 0.0, 75, 600, 1.3, 1.6, 0.03, 0.45).split(chr(10))
# TODO: understand all parameters above... see https://www.fon.hum.uva.nl/praat/manual/PointProcess__Get_jitter__ppq5____.html
rel_err = lambda Fix: abs((xdf[Fix]-fdf[Fix])/xdf[Fix]).mean()    # error relativo en valor absoluto

def FormStats(sound, pointProcess):
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")

    f1_list = [];    f2_list = [];    f3_list = [];    f4_list = []

    for point in range(0, numPoints):
        point += 1
        t = call(pointProcess, "Get time from index", point)
        f1 = call(formants, "Get value at time", 1, t, 'Hertz', 'Linear')
        f2 = call(formants, "Get value at time", 2, t, 'Hertz', 'Linear')
        f3 = call(formants, "Get value at time", 3, t, 'Hertz', 'Linear')
        f4 = call(formants, "Get value at time", 4, t, 'Hertz', 'Linear')
        f1_list.append(f1)
        f2_list.append(f2)
        f3_list.append(f3)
        f4_list.append(f4)

    f1_list = [f1 for f1 in f1_list if str(f1) != 'nan']
    f2_list = [f2 for f2 in f2_list if str(f2) != 'nan']
    f3_list = [f3 for f3 in f3_list if str(f3) != 'nan']
    f4_list = [f4 for f4 in f4_list if str(f4) != 'nan']

    # calculate mean formants across pulses
    f1_mean = statistics.mean(f1_list)
    f2_mean = statistics.mean(f2_list)
    f3_mean = statistics.mean(f3_list)
    f4_mean = statistics.mean(f4_list)

    return [statistics.mean(f) for f in (f1_list,f2_list,f3_list,f4_list)]
###############
def pesound(fn): 
    snd = parselmouth.Sound(fn)
    snd.pre_emphasize()
    return snd

def tryfloat(x):
    try:
        return float(x)
    except:
        return x
    
def voice_report(spp, FORMANTS=True):   # spp = [sound, pitch, pulses]
    # default values should be optional args
    #F0min, F0max = 50, 500   # should it match VoiceReport?
    #sound = parselmouth.Sound(filename)
    #pitch = sound.to_pitch()
    #pulses = call([sound, pitch], "To PointProcess (cc)")
    sound, pitch, pulses = spp
    voice_report_str = call(spp, "Voice report", 0.0, 0.0, F0min, F0max, 1.3, 1.6, 0.03, 0.45)
    
    vsplit = voice_report_str.split('\n')
    vdict = {vs.split(':')[0].strip(): vs.split(':')[1] 
            for vs in vsplit if len(vs.split(':'))>1 and vs.split(':')[1]!=''}
    # pass units from values to keys
    odict = dict()
    for k,v in vdict.items():
        vs = v.split()
        
        if len(vs)>1 and 'Fraction' not in k:
            if k[:4]=='From':
                odict['Duration [seconds]'] = float(vs[-2])
            else:
                nkey = f'{k} [{vs[-1]}]'
                odict[nkey] = ' '.join(vs[:-1])
        else:
            odict[k] = v.strip()  # fixes left space on Jitters+Shimmers
    odict = {k: tryfloat(v) for k,v in odict.items()}
    
    if FORMANTS:
        pointProcess = call(sound, "To PointProcess (periodic, cc)", F0min, F0max)
        fs = FormStats(sound, pointProcess)
        for ix in range(4):
            odict[f'F{ix+1}'] = fs[ix]
    
    return odict

class SoundData:

    def __init__(self, mask, preemp=False):
        self.files = sorted(list(glob.glob(mask)))
        self.nFiles = len(self.files)
        t0 = time.time()
        if preemp:
            self.sounds = list(map(pesound, self.files))
        else:
            self.sounds = list(map(parselmouth.Sound, self.files))

        print('mask:', mask, 'nFiles:', self.nFiles)
        self.pitches = [call(sound, "To Pitch", 0.0, F0min, F0max)
                        for sound in self.sounds]
        self.harmonicities = [call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
                        for sound in self.sounds]
        self.pointProcess = [call(sound, "To PointProcess (periodic, cc)", F0min, F0max)
                        for sound in self.sounds]
        self.pulses = [call([sound, pitch], "To PointProcess (cc)")
                        for sound, pitch in zip(self.sounds, self.pitches)]
        self.spp = zip(self.sounds, self.pitches, self.pulses)

        self.intensities = [sound.to_intensity() for sound in self.sounds]
        self.ppe = [PPE(sound) for sound in self.sounds]   # using PPE2
        # SOURCE: 
        dt0 = round(time.time()-t0, 2)
        print('INIT-dt:', dt0)

        t1 = time.time()
        self.process('CORFO')
        dt1 = round(time.time()-t1, 2)
        print('process-dt:', dt1)

    def process(self, varset):
        #self.spp = zip(self.sounds, self.pitches, self.pulses)
        #self.voicereps = list(map(voicerep, self.spp))
        self.voicereps = list(map(voice_report, self.spp))   
        self.df = pd.concat(pd.DataFrame(vr, index=[fn.split('/')[-1]]) 
                            for fn, vr in zip(self.files, self.voicereps))
        self.df['PPE'] = self.ppe

        self.df2 = self.df[['Mean pitch [Hz]', 'Maximum pitch [Hz]', 'Minimum pitch [Hz]', 'Jitter (local)', 'Jitter (local, absolute) [seconds]',  # 5/15
           'Jitter (rap)', 'Jitter (ppq5)', 'Shimmer (local)','Shimmer (local, dB) [dB]', 'Shimmer (apq3)', # 10/15
           'Shimmer (apq5)', 'Shimmer (apq11)', 'Mean harmonics-to-noise ratio [dB]', 'Mean noise-to-harmonics ratio', 'PPE']]   ## missing: MDVP:APQ?? 
        
        PERC_VARS = ['Jitter (rap)', 'Jitter (local)', 'Jitter (ppq5)', \
            'Shimmer (local)', 'Shimmer (apq3)', 'Shimmer (apq5)', 'Shimmer (apq11)']

        for var in PERC_VARS:
            print(self.df2[var])
            try:
                vdata = [0.01*float(xx.replace('%','')) for xx in self.df2[var]]
                self.df2.loc[:,var] = vdata
            except:
                self.df2.loc[:,var] = 'N/A'
        # predictions!
        #import pickle
        #model = pickle.load(open('pred_model.pk','rb'))
        #scaler = pickle.load(open('pred_scaler.pk','rb'))
        #self.ypred = model.predict(scaler.fit_transform(self.df2.values))

        #print('PRED:', self.ypred)
