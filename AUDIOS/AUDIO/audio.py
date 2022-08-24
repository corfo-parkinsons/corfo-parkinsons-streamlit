import time, glob
import numpy as np
import pandas as pd
from aws import upload_audio_to_s3  
from config import IN_FMT, OUT_FMT
from ppe import PPE
from pydub import AudioSegment
#from pydub.silence import split_on_silence

import parselmouth
from parselmouth.praat import call
import statistics
#import opensmile
################################################
def gender(fn):
    model = 'models/knn_speaker_male_female'
    c, p, p_nam = aT.file_classification(fn, model,'knn')
    return dict(zip(p_nam,p))

def freqs(fn):
    fs, s = aIO.read_audio_file(fn)
    duration = len(s) / float(fs)
    win, step = 0.050, 0.050
    [f, fn] = aF.feature_extraction(s, fs, int(fs * win), 
                                int(fs * step))
    print(f'{f.shape[1]} frames, {f.shape[0]} short-term features')
################################################
JS_COLUMNS = "F0, F0dev, hnr, nhr, localJit, localabsoluteJitter, rapJitter, \
        ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer,\
        apq11Shimmer, ddaShimmer, intensity, PPE".split(',')
JS_COLUMNS = [c.strip() for c in JS_COLUMNS]    

FKSTR = 'F1,F2,F3,F4' #, f1_median, f2_median, f3_median, f4_median'
FormKeys = [k.strip() for k in FKSTR.split(',')]
##################################################
def ogg2wav(ofn):
    wfn = ofn.replace(IN_FMT, OUT_FMT).replace(' ','_')
    x = AudioSegment.from_file(ofn)
    print('audio:OGG2WAV saving', wfn)
    x.export(wfn)    # was: 1022593114_1022593114359        maybe keep rez to make smaller
    
def ogg_to_jitters(file_name):    ## makes ogg and uploads
    ogg2wav(file_name)
    upload_audio_to_s3(file_name)
    out_file = file_name.replace(IN_FMT, OUT_FMT)
    print('computing Jitters:', out_file)
    js = JitterShimmer(out_file, True)
    return js
############### we need a class! vSound it is
class vSound:
    def __init__(self, filename):
        f0min, f0max = 75, 500   # MAKE UPPERCASE
        self.sound = parselmouth.Sound(filename)   # allows .wav and .mp3
        self.pitch = call(self.sound, "To Pitch", 0.0, f0min, f0max) 
        self.harmonicity = call(self.sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
        self.pointProcess = call(self.sound, "To PointProcess (periodic, cc)", f0min, f0max)
        self.pulses = call([self.sound, self.pitch], "To PointProcess (cc)")
        self.intensity = self.sound.to_intensity()
        
        self.process()

    def process(self, varset=''):
        sound, pitch, pulses, intensity = self.sound, self.pitch, self.pulses, self.intensity
        pointProcess = self.pointProcess
        
        self.voice_report_str = call([sound, pitch, pulses], 
                            "Voice report", 0.0, 0.0, 75, 600, 1.3, 1.6, 0.03, 0.45).split('\n')
        self.vrd={vv.split(':')[0].strip(): vv.split(':')[1].strip()
                     for vv in self.voice_report_str if ': ' in vv}
        
        intMean = intensity.get_average()
        meanF0 = call(pitch, "Get mean", 0, 0, "Hertz") # get mean pitch
        stdevF0 = call(pitch, "Get standard deviation", 0 ,0, "Hertz") # get standard deviation

        hnr = call(self.harmonicity, "Get mean", 0, 0)
        nhr = float(self.vrd['Mean noise-to-harmonics ratio'])

        localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
        localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
        rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
        ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
        ddpJitter = call(self.pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
        localShimmer =  call([sound, self.pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        localdbShimmer = call([sound, self.pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq3Shimmer = call([sound, self.pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        aqpq5Shimmer = call([sound, self.pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        apq11Shimmer =  call([sound, self.pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
        ddaShimmer = call([sound, self.pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    
        ppe = PPE(sound)	# NEU! as of June 1st 2022

        self.coefs = [meanF0, stdevF0, hnr, nhr, localJitter, localabsoluteJitter, rapJitter, \
            ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer,\
            apq11Shimmer, ddaShimmer, intMean, ppe]
        ### now the formants
        formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
        numPoints = call(pointProcess, "Get number of points")
    
        f1_list = [];    f2_list = [];    f3_list = [];    f4_list = []

        # Measure formants only at glottal pulses
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

        #f1_median = statistics.median(f1_list)
        #f2_median = statistics.median(f2_list)
        #f3_median = statistics.median(f3_list)
        #f4_median = statistics.median(f4_list)

        self.formants = [f1_mean, f2_mean, f3_mean, f4_mean]
                        #, f1_median, f2_median, f3_median, f4_median

    def get_JS(self, makedict=True):
        js = dict(zip(JS_COLUMNS, self.coefs))
        fdict = dict(zip(FormKeys, self.formants))
        js = {k: round(v,5) for k,v in js.items()}   # what if None?
        js.update(fdict)
        return js

def measurePitch(voiceID, f0min, f0max, unit):
    print('   *** MP0 ***')
    sound = parselmouth.Sound(voiceID) # read the sound
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max) 
    print('   *** MP 05 ***')
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    pulses = call([sound, pitch], "To PointProcess (cc)")
    print('   *** MP 007 ***')
    intensity = sound.to_intensity()
    ppe = PPE(sound)   # failing here??
    print('   *** MP1 ***')
    voice_report_str = call([sound, pitch, pulses], "Voice report", 0.0, 0.0, 75, 600, 1.3, 1.6, 0.03, 0.45).split('\n')
    vrd={vv.split(':')[0].strip(): vv.split(':')[1].strip()
         for vv in voice_report_str if ': ' in vv}
    print('   *** MP2 ***')
    #############################
    # pitch: F0(mean+dev
    # harm: hnr, nhr?
    intMean = intensity.get_average()
    
    meanF0 = call(pitch, "Get mean", 0, 0, unit) # get mean pitch
    stdevF0 = call(pitch, "Get standard deviation", 0 ,0, unit) # get standard deviation
    
    hnr = call(harmonicity, "Get mean", 0, 0)
    try:
        nhr = float(vrd['Mean noise-to-harmonics ratio'])
    except:
        print('VRD:', vrd)
        nhr = 0.000000001

    localJitter = call(pointProcess, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
    localabsoluteJitter = call(pointProcess, "Get jitter (local, absolute)", 0, 0, 0.0001, 0.02, 1.3)
    rapJitter = call(pointProcess, "Get jitter (rap)", 0, 0, 0.0001, 0.02, 1.3)
    ppq5Jitter = call(pointProcess, "Get jitter (ppq5)", 0, 0, 0.0001, 0.02, 1.3)
    ddpJitter = call(pointProcess, "Get jitter (ddp)", 0, 0, 0.0001, 0.02, 1.3)
    localShimmer =  call([sound, pointProcess], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    localdbShimmer = call([sound, pointProcess], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq3Shimmer = call([sound, pointProcess], "Get shimmer (apq3)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    aqpq5Shimmer = call([sound, pointProcess], "Get shimmer (apq5)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    apq11Shimmer =  call([sound, pointProcess], "Get shimmer (apq11)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    ddaShimmer = call([sound, pointProcess], "Get shimmer (dda)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
    print('   *** MPout ***')
    
    return (meanF0, stdevF0, hnr, nhr, localJitter, localabsoluteJitter, rapJitter, \
        ppq5Jitter, ddpJitter, localShimmer, localdbShimmer, apq3Shimmer, aqpq5Shimmer,\
        apq11Shimmer, ddaShimmer, intMean, ppe)

def measureFormants(sound, f0min,f0max):
    sound = parselmouth.Sound(sound) # read the sound
    pitch = call(sound, "To Pitch (cc)", 0, f0min, 15, 'no', 0.03, 0.45, 0.01, 0.35, 0.14, f0max)
    pointProcess = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    numPoints = call(pointProcess, "Get number of points")
    #print('NumPoints:', numPoints)

    f1_list = [];    f2_list = []
    f3_list = [];    f4_list = []
    
    # Measure formants only at glottal pulses
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
    
    #f1_median = statistics.median(f1_list)
    #f2_median = statistics.median(f2_list)
    #f3_median = statistics.median(f3_list)
    #f4_median = statistics.median(f4_list)
    
    return f1_mean, f2_mean, f3_mean, f4_mean #, f1_median, f2_median, f3_median, f4_median

def JitterShimmer(wave_file, makedict=False):
    sound = parselmouth.Sound(wave_file)

    js = measurePitch(sound, 75, 500, "Hertz")

    formants = measureFormants(sound, 75, 300)
    formdict = dict(zip(FormKeys, formants))

    if makedict:
        js = dict(zip(JS_COLUMNS,js))
        js = {k: round(v,5) for k,v in js.items()}   # what if None?
        js['Parkinson'] = 0.00001
        js.update(formdict)
        #js['F2/F1'] = round(js['F2']/js['F1'],2)
        # ahora SIN incluir valores de referencia
        #refs = {'F0': '[M=(100,165), F=(190,262)]',
        #        'F1': '[M=(718,906), F=(430,970)]',
        #        'F2': '[M=(1160,1300), F=(1380,1820)]',
        #        'F3': '[M=(2520,3020), F=(2750,3250)]',
        #        'F4': '[M=(3700,4250), F=(4050,4550)]',
                #'F2/F1': '[a=1.6,e=3.4,6.8,2.4]',
        #        'intensity': '[55,80]',
        #        'hnr': '[16.5, 20]', 'nhr': '[0.11, 0.19]',
        #       }
    return js

def runPCA(df):
    #Z-score the Jitter and Shimmer measurements
    features = ['localJitter', 'localabsoluteJitter', 'rapJitter', 'ppq5Jitter', 'ddpJitter',
         'localShimmer', 'localdbShimmer', 'apq3Shimmer', 'apq5Shimmer', 'apq11Shimmer', 'ddaShimmer']
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    #y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)
    #PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents, columns = ['JitterPCA', 'ShimmerPCA'])
    principalDf
    return principalDf



def os_mask(mask):
    smile = opensmile.Smile(
        feature_set=opensmile.FeatureSet.ComParE_2016,
        feature_level=opensmile.FeatureLevel.Functionals,
    )
    if '*' in mask:  # eg: 'bec*.wav'
        print('MASK:', mask)
        print('FILES:', list(glob.glob(mask)))
        y = smile.process_files(glob.glob(mask))
    else:
        y = smile.process_file(mask)
    return y

def os_down(mask, filename):
    y = os_mask(mask)
    y.to_excel(filename)
    print(f'{len(y)} files processed and saved to {filename}')

def wav2chunks(wavname, min_silence=200):

    sound = AudioSegment.from_wav(wavname)
    audio_chunks = split_on_silence(sound, min_silence_len=min_silence, silence_thresh=-40 )
    print(f'FOUND {len(audio_chunks)} chunks')
    return audio_chunks

def split_wav(wavname, filename):
    chunks = wav2chunks(wavname)
    for ix, chunk in enumerate(chunks):
        chunk.export(f'{filename}_{ix}.wav', format='wav')
    print(f'SAVED {len(chunks)} chunks to {filename}*')
    
import math

def quad_area(F1,F2):       # computing quadrilateral area for Bang et al
    a,b,c,d = [math.sqrt((F1[ix]-F1[ix-1])**2+(F2[ix]-F2[ix-1])**2)
               for ix in range(4)]
                       
    semiperimeter = (a + b + c + d) / 2

    return math.sqrt((semiperimeter - a) *
                    (semiperimeter - b) *
                    (semiperimeter - c) * 
                    (semiperimeter - d))
