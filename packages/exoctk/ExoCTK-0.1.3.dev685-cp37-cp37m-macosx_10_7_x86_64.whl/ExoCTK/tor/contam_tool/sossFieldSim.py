from astroquery.irsa import Irsa
import matplotlib.pyplot as plt
import generate_JH_HK_colors as colors
import astropy.coordinates as crd
import astropy.units as u
import numpy as np
import os, glob, idlsave, pdb

def sossFieldSim(ra, dec, binComp=None):

	# binComp=[deltaRA,deltaDEC,J,H,K]

	# stars in large field around target
	targetcrd = crd.SkyCoord(ra = ra, dec = dec, unit=(u.hour, u.deg))
	targetRA = targetcrd.ra.value
	targetDEC = targetcrd.dec.value
	info   = Irsa.query_region(targetcrd, catalog = 'fp_psc', spatial = 'Box', width = 4*u.arcmin) 
	# coordinates of possible contaminants in degrees
	contamRA   = info['ra'].data.data 
	contamDEC  = info['dec'].data.data
	Jmag        = info['j_m'].data.data
	Hmag        = info['h_m'].data.data
	Kmag        = info['k_m'].data.data
	J_Hobs      = (Jmag-Hmag)
	H_Kobs      = (Hmag-Kmag)
	
	# target coords
	distance    = np.sqrt((targetRA-contamRA)**2 + (targetDEC-contamDEC)**2)
	targetIndex = np.argmin(distance) # the target
	
	# add any missing companion
	cubeNameSuf=''
	if binComp is not None:
		#contamRA       = [contamRA,contamRA[targetIndex]+bincomp[0]/3600/cos(contamDEC[targetIndex]*!dtor)] (JF)
		deg2rad = np.pi/180
		contamRA    = np.append(contamRA, (contamRA[targetIndex] + binComp[0]/3600/cos(contamDEC[targetIndex]*deg2rad)))
		contamDEC   = np.append(contamDEC, (contamDEC[targetIndex] + binComp[1]/3600))
		Jmag        = np.append(Jmag,binComp[2])
		Hmag        = np.append(Kmag,binComp[3])
		Kmag        = np.append(Kmag,binComp[4])
		J_Hobs      = (Jmag-Hmag)
		H_Kobs      = (Hmag-Kmag)
		cubeNameSuf ='_custom'

	#Joe's coordinate conversion code
	def deg2HMS(ra='', dec='', round=False):
		RA, DEC, rs, ds = '', '', '', ''
		if dec:
			if str(dec)[0] == '-':
		  		ds, dec = '-', abs(dec)
			deg = int(dec)
			decM = abs(int((dec-deg)*60))
			if round:
		  		decS = int((abs((dec-deg)*60)-decM)*60)
			else:
		  		decS = (abs((dec-deg)*60)-decM)*60
			DEC = '{0}{1} {2} {3}'.format(ds, deg, decM, decS)

		if ra:
			if str(ra)[0] == '-':
		  		rs, ra = '-', abs(ra)
			raH = int(ra/15)
			raM = int(((ra/15)-raH)*60)
			if round:
		  		raS = int(((((ra/15)-raH)*60)-raM)*60)
			else:
		  		raS = ((((ra/15)-raH)*60)-raM)*60
			RA = '{0}{1} {2} {3}'.format(rs, raH, raM, raS)

		if ra and dec:
			return (RA, DEC)
		else:
			return RA or DEC

	cubeName = 'cubes/cube_RA' + deg2HMS(ra = contamRA[targetIndex], round = True) + \
	                     'DEC' + deg2HMS(ra = contamDEC[targetIndex], round = True) + cubeNameSuf + '.fits'

	print('Cube name:')
	print(cubeName)
	print('cubNameSuf:')
	print(cubeNameSuf)
	print('Target coordinates:')
	print(deg2HMS(ra = contamRA[targetIndex]))
	print(deg2HMS(ra = contamDEC[targetIndex]))


	if os.path.exists(cubeName) and (binComp is not None):
		return

	
	"""
	# the trace models
	if 0:
		modelDir  = '/Users/david/Documents/work/jwst/a_GTO/SOSS-WG/contamination/modelTraces'

		# synthetic mag & colors of models
		readcol,modelDir+'/'+'magnitude_modele_atm.txt',Ttheo,logg,MH,aH,Jtheo,Htheo,Ktheo,jhtheo,jktheo,hktheo,format='f,f,f,f,f,f,f,f,f,f'
		remove,where(logg ne 4.50 or Ttheo lt 2800),Ttheo,logg,jhtheo,jktheo,hktheo 

		# load model traces
		fNameMod=file_search(modelDir,'simu_lte*-4.5-0.0.BT-Settl_LLNL_UDEMPSF_cropped.fits.gz',count=nMod)
		teffMod=fix(strmid(fNameMod,strpos(fNameMod[0],'simu_lte')+8,3))*100
		isort=sort(teffMod)
		teffMod=teffMod[isort]
		fNameMod=fNameMod[isort]

		# cropped model traces are cubes whose third axis are: 0->sum of all orders, 1->order 1, 2->order 2
		h0=headfits(fNameMod[0])
		dimXmod=sxpar(h0,'naxis1')
		dimYmod=sxpar(h0,'naxis2')
		models=fltarr(dimXmod,dimYmod,nMod)
		jhMod=fltarr(nMod)
		hkMod=fltarr(nMod)
		for i=0,nMod-1 do begin
			tmp=readfits(fNameMod[i])
			models[*,*,i]=tmp[*,*,0] # keep only the sum of all orders

			modelO12=tmp[*,*,1:2]
			fNameModO12='modelOrder12_teff'+strtrim(teffMod[i],2)+'.sav'
			save,modelO12,file=fNameModO12
		
			j=where(Ttheo eq teffMod[i])
			jhMod[i]=jhTheo[j]
			hkMod[i]=hkTheo[j]	
		endfor
		modelPadX = 2000-1900
		modelPadY = 2000

		# save the model traces
		save,models,fNameModO12,teffMod,jhMod,hkMod,dimXmod,dimYmod,modelPadX,modelPadY,Ttheo,logg,jhtheo,jktheo,hktheo,file='modelsInfo.sav'
	endif else begin
		restore,'modelsInfo.sav'
	endelse
	"""

	# Initialize final fits cube that contains the modelled traces with contamination
	PAmin = 0
	PAmax = 360
	angle_step = 1	# degrees
	# Set of fov angles to cover
	angle_set = np.arange(PAmin, PAmax+angle_step, angle_step)	# degrees
	nsteps    = len(angle_set)
	simucube  = np.zeros((256,2048,nsteps+2))  # cube of trace simulation at every degree of field rotation,+target at O1 and O2

	#pos_dict  = dict(x=99.9,y=99.9,contamRA=99.9,contamDEC=99.9,jmag=99.9)
	niriss_pixel_scale = 0.065	# arcsec

	sweetspot = dict(x=99.9,y=99.9,contamRA=99.9,contamDEC=99.9,jmag=99.9)
	sweetspot['x'] = 859			# position on the detector of the target in direct images
	sweetspot['y'] = 107
	sweetspot['contamRA'] = contamRA[targetIndex]
	sweetspot['contamDEC'] = contamDEC[targetIndex]
	sweetspot['jmag'] = Jmag[targetIndex]

	# Put field stars position and magnitudes in a dictture
	nstars = len(contamRA)
	stars = dict(x=np.empty(nstars), y=np.empty(nstars), contamRA=np.empty(nstars), contamDEC=np.empty(nstars), jmag=np.empty(nstars))
	
	stars['contamRA']  = contamRA
	stars['contamDEC'] = contamDEC
	stars['jmag'] = Jmag

	# find Teff of each star
	T = np.zeros(nstars)
	jhMod, hkMod, teffMod = colors.colorMod()
	#Question JF: what if len(nstars)!=len(jhMod)?
	for j in range(nstars):
		color_seperation = (J_Hobs[j]-jhMod)**2+(H_Kobs[j]-hkMod)**2
		min_seperation_ind = np.argmin(color_seperation)
		T[j]=teffMod[min_seperation_ind]

	# load8colors
	# Big loop to generate a simulation at each Field-of-view (FOV) rotation
	radeg = 180/np.pi
	for angle in angle_set:
		fieldrotation = angle
	# 	print('Angle:',fieldrotation

		pixelsep = 3600 * np.sqrt((np.cos(sweetspot['contamDEC']/radeg)*((stars['contamRA'] - sweetspot['contamRA']))**2)+((stars['contamDEC'] - sweetspot['contamDEC'])**2))
		xo = -np.cos(sweetspot['contamDEC']/radeg)*(stars['contamRA'] - sweetspot['contamRA'])*3600/niriss_pixel_scale
		yo = (stars['contamDEC'] - sweetspot['contamDEC'])*3600/niriss_pixel_scale

		dx = xo * np.cos(fieldrotation/radeg) - yo * np.sin(fieldrotation/radeg)
		dy = xo * np.sin(fieldrotation/radeg) + yo * np.cos(fieldrotation/radeg)
	
		stars['x'] = dx+sweetspot['x']
		stars['y'] = dy+sweetspot['y']
 
	        # email from Michael Maszkiewicz on 2016 May 17:
	        #  POM edge is:
	        #     1.67-2.01 mm left of detector in x
	        #     2.15-2.22 mm above detector in y
	        #     2.22-2.43 mm right of detector in x
	        #     1.49-1.87 mm below detector in y
	        #  we take the larger value in each direction and add a 50 pixels margin
	        #  given the uncertainty of the POM location wrt to detector FOV
		# Retain stars that are within the Direct Image NIRISS POM FOV
		
		ind = np.where((stars['x'] >= -162) & (stars['x'] <= 2047+185) & (stars['y'] >= -154) & (stars['y'] <= 2047+174))
		starsInFOV = dict(x=stars['x'][ind], y =stars['y'][ind], contamRA=stars['contamRA'][ind], contamDEC=stars['contamDEC'][ind], jmag=stars['jmag'][ind]) # *** pour In Field Of View
		dx = dx[ind]
		dy = dy[ind]
		Tboucle = T[ind]
		
		
	
	# 	print(' Number of stars in FOV:',nstars # ***
	# 	print(' J magnitude of those stars:', starsInFOV.jmag # ***
	# 	print(' Temperature of those stars:', Tboucle

		# print
		# printline,starsInFOV.x,starsInFOV.y,starsInFOV.jmag

		if 0 & nstars > 1:
			# Display the star field and sub array location in red
			plt.plot(starsInFOV['x'], starsInFOV['y'], 'o')
			plt.xlim(-50,2047+50)
			plt.ylim(-50,2047+50)
			plt.plot([0,2047,2047,0,0],[0,0,2047,2047,0], 'r')
			plt.plot([0,255,255,0,0],[0,0,2047,2047,0], 'g')
			plt.plot(sweetspot['x'], sweetspot['y'], 'ro')
			plt.show()

		saveFiles = glob.glob('idlSaveFiles/*.sav')[:-1]
		modelPadX = 2000-1900
		modelPadY = 2000
		dimXmod = 256
		dimYmod = 2048
		for i in range(len(ind)):
			intx = round(dx[i])
			inty = round(dy[i])
			# print(intx,inty
		
			k=np.where(teffMod == Tboucle[i])
			
			
			fluxscale = 10.0**(-0.4*(starsInFOV['jmag'][i] - sweetspot['jmag']))
			

			# if target and first angle, add target traces of order 1 and 2 in output cube
			if (intx == 0) and (inty == 0) and (ang == 0):
				# modelO1O2=readfits(fNameMod[k]) # read the order 1 and order 2 trace
				fNameModO12 = saveFiles[i]
				modelO12 = idlsave.read(fNameModO12)
				simucube[0, :, :]= modelO12[0, modelPadY:modelPadY+2047, modelPadX:modelPadX+255] * fluxscale # order 1
				simucube[1, :, :]= modelO12[1, modelPadY:modelPadY+2047, modelPadX:modelPadX+255] * fluxscale # order 2
		
			# if a field star
			
			if (intx != 0) or (inty != 0):
				mx0=modelPadX-intx
				mx1=modelPadX-intx+255
				my0=modelPadY-inty
				my1=modelPadY-inty+2047
				#pdb.set_trace()
				if (mx0 > dimXmod-1) or (my0 > dimYmod-1):
					continue
				if (mx1 < 0) or (my1 < 0):
					continue
				x0=(-mx0)>0
				y0=(-my0)>0
				mx0>=0
				mx1<=(dimXmod-1)
				my0>=0
				my1<=(dimYmod-1)
				simucube[angle_set+2, y0:y0+my1-my0, x0:x0+mx1-mx0] += models[mx0:mx1,my0:my1,k] * fluxscale
	
	fits.writeto(cubeName, simucube, overwrite = True) 