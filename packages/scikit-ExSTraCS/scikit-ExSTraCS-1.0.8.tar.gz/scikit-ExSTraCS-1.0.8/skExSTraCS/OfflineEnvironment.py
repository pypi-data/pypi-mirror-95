from skExSTraCS.DataManagement import DataManagement

class OfflineEnvironment:
    def __init__(self,features,phenotypes,model):
        """Initialize Offline Environment"""
        self.dataRef = 0
        self.formatData = DataManagement(features,phenotypes,model)

        self.currentTrainState = self.formatData.trainFormatted[0][self.dataRef]
        self.currentTrainPhenotype = self.formatData.trainFormatted[1][self.dataRef]

    def getTrainInstance(self):
        return (self.currentTrainState,self.currentTrainPhenotype)

    def newInstance(self):
        if self.dataRef < self.formatData.numTrainInstances-1:
            self.dataRef+=1
            self.currentTrainState = self.formatData.trainFormatted[0][self.dataRef]
            self.currentTrainPhenotype = self.formatData.trainFormatted[1][self.dataRef]
        else:
            self.resetDataRef()

    def resetDataRef(self):
        self.dataRef = 0
        self.currentTrainState = self.formatData.trainFormatted[0][self.dataRef]
        self.currentTrainPhenotype = self.formatData.trainFormatted[1][self.dataRef]
