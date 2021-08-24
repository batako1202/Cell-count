from ij import IJ
from ij.plugin.frame import RoiManager
from ij.plugin.filter import ParticleAnalyzer, BackgroundSubtracter, EDM, MaximumFinder
from ij.measure import ResultsTable
from ij.io import DirectoryChooser
from ij.plugin import ContrastEnhancer, Thresholder, ImageCalculator
import os
import shutil
from trainableSegmentation import WekaSegmentation

#NeuN count

def NeuNAnalyzer(filepath):
    """ Loads trained classifier and segments cells """ 
    """	in aligned images according to training.    """
    imp = IJ.openImage(filepath)
    # Subtract Background
    bs = BackgroundSubtracter()
    ip = imp.getProcessor()
    bs.rollingBallBackground(ip, 50.0, False, False, False, True, True)
	# Sharpen Image
    IJ.run(imp, "Unsharp Mask...", "radius=50 mask=0.30")
    IJ.run(imp, "Gamma...", "value=1.30")
    IJ.run(imp, "Enhance Contrast", "saturated=10.0")
    
    # Remove noise
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Smooth", "")
    IJ.run(imp, "Kuwahara Filter", "sampling=3")
    IJ.run(imp, "Remove Outliers...", "radius=3 threshold=50 which=Bright")
    
    # Define reference image for segmentation (default is timepoint000).
    weka = WekaSegmentation()
    weka.setTrainingImage(imp)
    
    # Select classifier model
    weka.loadClassifier("/Volumes/NO NAME/classifier5.model")
    weka.applyClassifier(False)
    imp = weka.getClassifiedImage()
    
    rm = RoiManager().getInstance2()
    rt = ResultsTable()
    
    # duplicate imp, make binary
    binimp = imp.duplicate()
    IJ.setThreshold(binimp, 0, 0, "Black&White")
    Thresholder().createMask(binimp)
    
    # remove noize
    IJ.run(binimp, "Make Binary", "")
    IJ.run(binimp, "Fill Holes", "")
    IJ.run(binimp, "Open", "")
    EDM().toWatershed(binimp.getProcessor())
    
    # Analyze particles
    IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
    PA = ParticleAnalyzer(11, 0, rt, 30, 10000, 0, 1.0)
    PA.setRoiManager(rm)
    PA.analyze(binimp)
    IJ.log("Number of cells = "+str(rm.getCount()))

    # save results
    savefilepath = filepath[:-4]+"_"
    rm.runCommand("Save", savefilepath + "Roi.zip")
    rt.saveAs(savefilepath + "Result.csv")
    IJ.saveAs(binimp, "bmp", savefilepath + "AnalyzedResult.bmp") 

    # close roi manager, results table and images
    rm.close()
    imp.close()
    binimp.close()


# Open dialog to choose folder
srcDir = DirectoryChooser("Choose directory").getDirectory()
IJ.log("directory: " + srcDir)

# search tif file in srcDir and analyze tif file by RiceAnalyzer()
for root, directories, filenames in os.walk(srcDir):
    for filename in filenames:
        if filename.endswith("z3_Cy5_1.tif") or filename.endswith("z03_Cy5_1.tif") and not filename.startswith("."):
            imagefilepath = os.path.join(root, filename)
            IJ.log("Image file path: " + imagefilepath)
            NeuNAnalyzer(imagefilepath)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of NeuN.csv") 


def Tdtomato(filepath):
	""" Loads trained classifier and segments cells """ 
	"""	in aligned images according to training.    """
	train = IJ.openImage(filepath)
	bs = BackgroundSubtracter()
	ip = train.getProcessor()
	bs.rollingBallBackground(ip, 50.0, False, False, False, True, True)
	IJ.run(train, "Enhance Contrast", "saturated=0")
    
	# Define reference image for segmentation (default is timepoint000).
	weka = WekaSegmentation()
	weka.setTrainingImage(train)
	
	# Select classifier model.
	weka.loadClassifier("/Volumes/NO NAME/classifier5.model")
	weka.applyClassifier(False)
	imp = weka.getClassifiedImage()
	
	rm = RoiManager().getInstance2()
	rt = ResultsTable()
	
	# duplicate imp, make binary
	binimp = imp.duplicate()
	IJ.setThreshold(binimp, 0, 0, "Black&White")
	Thresholder().createMask(binimp)
	# remove noize
	IJ.run(binimp, "Make Binary", "")
	IJ.run(binimp, "Open", "")
	
	# Analyze particles
	IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
	PA = ParticleAnalyzer(11, 0, rt, 30, 10000, 0, 1.0)
	PA.setRoiManager(rm)
	PA.analyze(binimp)
	IJ.log("Number of cells = "+str(rm.getCount()))
	
	# save results
	savefilepath = filepath[:-4]+"_"
	rm.runCommand("Save", savefilepath + "Roi.zip")
	rt.saveAs(savefilepath + "Result.csv")
	IJ.saveAs(binimp, "bmp", savefilepath + "AnalyzedResult.bmp") 
	
    # close roi manager, results table and images
	rm.close()
	imp.close()
	binimp.close()

# search tif file in srcDir and analyze tif file
for root, directories, filenames in os.walk(srcDir):
    for filename in filenames:
        if filename.endswith("Rhodamine_2.tif") and not filename.startswith(".") and ("Orthogonal") in filename :
            filepath = os.path.join(root, filename)
            IJ.log("Image file path: " + filepath)
            Tdtomato(filepath)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of Astrocyte.csv")
            

            
#Astrocyte count(single section)

def Weka_Segm(filepath):
	""" Loads trained classifier and segments cells """ 
	"""	in aligned images according to training.    """
	train = IJ.openImage(filepath)
	IJ.run(train, "Enhance Contrast", "saturated=0")
	# Define reference image for segmentation (default is timepoint000).
	weka = WekaSegmentation()
	weka.setTrainingImage(train)
	
	# Select classifier model.
	weka.loadClassifier("/Volumes/NO NAME/classifier5.model")
	weka.applyClassifier(False)
	imp = weka.getClassifiedImage()
	
	rm = RoiManager().getInstance2()
	rt = ResultsTable()
	
	# duplicate imp, make binary
	binimp = imp.duplicate()
	IJ.setThreshold(binimp, 0, 0, "Black&White")
	Thresholder().createMask(binimp)
	# remove noize
	IJ.run(binimp, "Make Binary", "")
	IJ.run(binimp, "Open", "")
	
	# Analyze particles
	IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
	PA = ParticleAnalyzer(11, 0, rt, 30, 10000, 0, 1.0)
	PA.setRoiManager(rm)
	PA.analyze(binimp)
	IJ.log("Number of cells = "+str(rm.getCount()))
	
	# save results
	savefilepath = filepath[:-4]+"_"
	rm.runCommand("Save", savefilepath + "Roi.zip")
	rt.saveAs(savefilepath + "Result.csv")
	IJ.saveAs(binimp, "bmp", savefilepath + "AnalyzedResult_single.bmp") 
	
    # close roi manager, results table and images
	rm.close()
	imp.close()
	binimp.close()

# search tif file in srcDir and analyze tif file
for root, directories, filenames in os.walk(srcDir):
    for filename in filenames:
        if filename.endswith("z3_Rhodamine_2.tif") or filename.endswith("z03_Rhodamine_2.tif") and not filename.startswith("."):
            filepath = os.path.join(root, filename)
            IJ.log("Image file path: " + filepath)
            Weka_Segm(filepath)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of Astrocyte(single section).csv")

#s100 count

def CellAnalyzer(imagefilepath2):
    # open image, set roi manager and set result table
    imp = IJ.openImage(imagefilepath2)
    IJ.run(imp, "Enhance Contrast", "saturated=0")
    # Subtract Background
    bs = BackgroundSubtracter()
    ip = imp.getProcessor()
    bs.rollingBallBackground(ip, 10.0, False, False, False, True, True)
    IJ.run(imp, "16-bit", "")
	# Sharpen Image
    IJ.run(imp, "Unsharp Mask...", "radius=10 mask=0.60")
    IJ.run(imp, "Gamma...", "value=1.50")
    ContrastEnhancer().stretchHistogram(imp, 0.3)
    
    # Remove noise
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Despeckle", "")
    IJ.run(imp, "Smooth", "")
    IJ.run(imp, "Kuwahara Filter", "sampling=3")
    IJ.run(imp, "Remove Outliers...", "radius=3 threshold=50 which=Bright")
    
    rm = RoiManager().getInstance2()
    rt = ResultsTable()

    # duplicate imp, make binary and run watershed
    binimp = imp.duplicate()
    IJ.setAutoThreshold(binimp, "Huang dark")
    IJ.run(binimp, "Make Binary", "thresholded remaining")
    IJ.run(binimp,"Open", "")
    EDM().toWatershed(binimp.getProcessor())
	
    # Analyze particles
    IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
    PA = ParticleAnalyzer(11, 0, rt, 30, 1000, 0, 1.0)
    PA.setRoiManager(rm)
    PA.analyze(binimp)
    IJ.log("Number of cells = "+str(rm.getCount()))
	
    # save results 	
    savefilepath = imagefilepath2[:-4]+"_"
    rm.runCommand("Save", savefilepath + "Roi.zip")
    rt.saveAs(savefilepath + "Result.csv")
    IJ.saveAs(binimp, "bmp", savefilepath + "AnalyzedResult.bmp")
	
    # close roi manager, results table and images
    rm.close()
    imp.close()
    binimp.close()

for root, directories, filenames in os.walk(srcDir):
    for filename2 in filenames:
        if filename2.endswith("EGFP_3.tif") and not filename2.startswith(".") and "Orthogonal" in filename2 :
            imagefilepath2 = os.path.join(root, filename2)
            IJ.log("Image file path: " + imagefilepath2)
            CellAnalyzer(imagefilepath2)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of S100.csv") 


#S100 merge count
def MergeAnalyzer(filepath1,filepath2):
	imp1 = IJ.openImage(filepath1)
	imp2 = IJ.openImage(filepath2)
	imp3 = ImageCalculator().run("AND create", imp1, imp2)
	rm = RoiManager().getInstance2()
	rt = ResultsTable()
	# duplicate imp, make binary
	binimp = imp3.duplicate()
	# remove noize
	IJ.run(binimp, "Make Binary", "")
	IJ.run(binimp, "Open", "")
	# Analyze particles
	IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
	PA = ParticleAnalyzer(11, 0, rt, 30, 10000, 0, 1.0)
	PA.setRoiManager(rm)
	PA.analyze(binimp)
	IJ.log(str(rm.getCount()))
	
	# save results
	savefilepath = root + "/"
	rm.runCommand("Save", savefilepath + "merge_Roi.zip")
	rt.saveAs(savefilepath + "merge_Result.csv")
	IJ.saveAs(binimp, "bmp", savefilepath + "merge_AnalyzedResult.bmp") 
	
    # close roi manager, results table and images
	rm.close()
	binimp.close()

# search tif file in srcDir and analyze tif file by RiceAnalyzer()
for root, directories, filenames in os.walk(srcDir):
    for filename in filenames:
         if filename.endswith("EGFP_3_AnalyzedResult.bmp") and not filename.startswith("."):
            filepath1 = os.path.join(root, filename)
            filepath2 = os.path.join(root, filename[:-25] + "Rhodamine_2_AnalyzedResult.bmp")
            MergeAnalyzer(filepath1,filepath2)
            shutil.move(filepath1, "/Volumes/NO NAME/S100 bmp image for triple merge")
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of merge.csv")
                        
def Triplemerge(filepath1,filepath2):
	imp1 = IJ.openImage(filepath1)
	imp2 = IJ.openImage(filepath2)
	imp4 = IJ.openImage(filepath3)
	imp3 = ImageCalculator().run("AND create", imp1, imp2)
	imp5 = ImageCalculator().run("AND create", imp3, imp4)
	rm = RoiManager().getInstance2()
	rt = ResultsTable()
	# duplicate imp, make binaryOlig2 
	binimp = imp5.duplicate()
	# remove noize
	IJ.run(binimp, "Make Binary", "")
	IJ.run(binimp, "Open", "")
	# Analyze particles
	IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
           
	PA = ParticleAnalyzer(11, 0, rt, 20, 10000, 0, 1.0)
	PA.setRoiManager(rm)
	PA.analyze(binimp)
	IJ.log(str(rm.getCount()))
	
	# save results
	savefilepath = root + "/"
	rm.runCommand("Save", savefilepath + "Triple_merge_Roi.zip")
	rt.saveAs(savefilepath + "Triple_merge_Result.csv")
	IJ.saveAs(binimp, "bmp", savefilepath + "Triple_merge_AnalyzedResult.bmp") 
	
	# close roi manager, results table and images
	rm.close()
	binimp.close()
	
# search tif file in srcDir and analyze tif file by RiceAnalyzer()
for root, directories, filenames in os.walk(srcDir):
    for filename2 in filenames:
        if filename2.endswith("EGFP_3.tif") and not filename2.startswith(".") and "Orthogonal" in filename2 :
            imagefilepath2 = os.path.join(root, filename2)
            IJ.log("Image file path: " + imagefilepath2)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of S100.csv") 
            for root, directories, filenames in os.walk(srcDir):
            	for filename in filenames:
            		if filename.endswith("Cy5_1_AnalyzedResult.bmp") and not filename.startswith(".") and filename2[:-52] in filename :
            			filepath1 = os.path.join(root, filename)
            			filepath2 = os.path.join(root, filename[:-24] + "Rhodamine_2_AnalyzedResult_single.bmp")
            			os.rename(os.path.join("/Volumes/NO NAME/S100 bmp image for triple merge", filename2[:-10] + "EGFP_3_AnalyzedResult.bmp"), os.path.join("/Volumes/NO NAME/S100 bmp image for triple merge", filename[:-24] +"EGFP_3_AnalyzedResult.bmp"))
            			filepath3 = os.path.join("/Volumes/NO NAME/S100 bmp image for triple merge", filename[:-24] +"EGFP_3_AnalyzedResult.bmp")
            			Triplemerge(filepath1,filepath2)
            			IJ.saveAs("Results", "/Volumes/NO NAME/Result of triple merge.csv")
            			
#NeuN merge count
def NeuNmerge(filepath1,filepath2):
	imp1 = IJ.openImage(filepath1)
	imp2 = IJ.openImage(filepath2)
	imp3 = ImageCalculator().run("AND create", imp1, imp2)
	rm = RoiManager().getInstance2()
	rt = ResultsTable()
	# duplicate imp, make binaryOlig2 
	binimp = imp3.duplicate()
	# remove noize
	IJ.run(binimp, "Make Binary", "")
	IJ.run(binimp, "Open", "")
	# Analyze particles
	IJ.run("Set Measurements...",
           "area  centroid fit redirect=None decimal=3")
           
	PA = ParticleAnalyzer(11, 0, rt, 20, 10000, 0, 1.0)
	PA.setRoiManager(rm)
	PA.analyze(binimp)
	IJ.log(str(rm.getCount()))
	
	# save results
	savefilepath = root + "/"
	rm.runCommand("Save", savefilepath + "NeuN_merge_Roi.zip")
	rt.saveAs(savefilepath + "NeuN_merge_Result.csv")
	IJ.saveAs(binimp, "bmp", savefilepath + "NeuN_merge_AnalyzedResult.bmp") 
	
	# close roi manager, results table and images
	rm.close()
	binimp.close()

# search tif file in srcDir and analyze tif file by RiceAnalyzer()
for root, directories, filenames in os.walk(srcDir):
    for filename in filenames:
         if filename.endswith("Cy5_1_AnalyzedResult.bmp") and not filename.startswith(".") :
            filepath1 = os.path.join(root, filename)
            filepath2 = os.path.join(root, filename[:-24] + "Rhodamine_2_AnalyzedResult_single.bmp")
            NeuNmerge(filepath1,filepath2)
            IJ.saveAs("Results", "/Volumes/NO NAME/Result of NeuN merge.csv")

IJ.log("finish!")