import FWCore.ParameterSet.Config as cms

#isDebug = True
isDebug = False
useData = False
#useData = True
if useData:
    met_sources_GL =  cms.vstring("slimmedMETs","slimmedMETsPuppi","slMETsCHS","slimmedMETsMuEGClean","slimmedMETsEGClean","slimmedMETsUncorrected")
else:
    met_sources_GL =  cms.vstring("slimmedMETs","slimmedMETsPuppi","slMETsCHS","slimmedMETsMuEGClean")

# minimum pt for the large-R jets (applies for all: vanilla CA8/CA15, cmstoptag, heptoptag). Also applied for the corresponding genjets.
fatjet_ptmin = 150.0
#fatjet_ptmin = 10.0 #TEST

bTagDiscriminators = [
    'pfJetProbabilityBJetTags',
    'pfJetBProbabilityBJetTags',
    'pfSimpleSecondaryVertexHighEffBJetTags',
    'pfSimpleSecondaryVertexHighPurBJetTags',
    'pfCombinedInclusiveSecondaryVertexV2BJetTags',
    'pfCombinedMVAV2BJetTags',
    'pfBoostedDoubleSecondaryVertexAK8BJetTags',
    'pfBoostedDoubleSecondaryVertexCA15BJetTags'
]


bTagInfos = [
    'pfImpactParameterTagInfos'
   ,'pfSecondaryVertexTagInfos'
   ,'pfInclusiveSecondaryVertexFinderTagInfos'
   ,'softPFMuonsTagInfos'
   ,'softPFElectronsTagInfos'
]

process = cms.Process("USER")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)
#process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1)
#irene:
#process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) , allowUnscheduled = cms.untracked.bool(True), SkipEvent = cms.untracked.vstring('ProductNotFound') )
#before it was process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) , allowUnscheduled = cms.untracked.bool(True)
#irene added SkipEvent = cms.untracked.vstring('ProductNotFound')
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) , allowUnscheduled = cms.untracked.bool(True))# , SkipEvent = cms.untracked.vstring('ProductNotFound'))

# DEBUG ----------------
if isDebug:
    process.Timing = cms.Service("Timing",
    summaryOnly = cms.untracked.bool(False),
    useJobReport = cms.untracked.bool(True)
    )

    process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
    ignoreTotal = cms.untracked.int32(2),                                            
    moduleMemorySummary = cms.untracked.bool(True)
    )

# DEBUG ----------------

process.source = cms.Source("PoolSource",
  fileNames  = cms.untracked.vstring([

           #'/store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16RAWAODSIM_reHLT_80X_mcRun2_asymptotic_v14_ext3-v1/00000/0064B539-803A-E611-BDEA-002590D0B060.root' #MC test file
#           '/store/mc/RunIISpring16MiniAODv2/TT_TuneCUETP8M1_13TeV-powheg-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext3-v2/70000/00287FF4-0E40-E611-8D06-00266CFE78EC.root'
#           '/store/mc/RunIISummer16MiniAODv2/QCD_Pt_15to6500_FwdEnriched_TuneCUETP8M1_13TeV_pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/26DF5A94-14BE-E611-99FC-0CC47A78A3EE.root'
#irene            'store/mc/RunIISummer16MiniAODv2/BulkGravToWWToWlepWhad_narrow_M-2000_13TeV-madgraph/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/80000/F6EF3B47-1AB7-E611-994D-0025904C7A54.root'
# irene, no upgrade, with pileup 
'file:/nfs/dust/cms/user/zoiirene/UpgradeStudiesGtoWW/Phase1/step3_inMINIAODSIM.root'
#'file:/nfs/dust/cms/user/zoiirene/UpgradeStudiesGtoWW/Phase1/step3_inMINIAODSIM.root'
           # '/store/mc/RunIISummer16MiniAODv2/ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6_ext1-v1/50000/3495D426-73C1-E611-B11B-0CC47A4D764A.root'
           #'/store/data/Run2016B/JetHT/MINIAOD/PromptReco-v2/000/273/503/00000/069FE912-3E1F-E611-8EE4-02163E011DF3.root'
           #'/store/data/Run2016B/SingleMuon/MINIAOD/PromptReco-v2/000/273/150/00000/34A57FB8-D819-E611-B0A4-02163E0144EE.root'
  ]),
  skipEvents = cms.untracked.uint32(0)
)
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(300))
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000))
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10000))
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50000))

# Grid-control changes:
gc_maxevents = '__MAX_EVENTS__'
gc_skipevents = '__SKIP_EVENTS__'
gc_filenames = '__FILE_NAMES__'

import os
gc_nickname = os.getenv('DATASETNICK')

if gc_nickname is not None:
    useData = not gc_nickname.startswith('MC_')
    process.source.fileNames = map(lambda s: s.strip(' "'), gc_filenames.split(','))
    process.source.skipEvents = int(gc_skipevents)
    process.maxEvents.input = int(gc_maxevents)

#process.source.skipEvents = int(30000) #TEST

###############################################
# OUT
from Configuration.EventContent.EventContent_cff import *
process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('miniaod.root'),
                               outputCommands = MINIAODSIMEventContent.outputCommands )

process.out.outputCommands.extend([ 
    'keep *_patJetsAk8CHS*_*_*',
    'keep *_patJetsAk8Puppi*_*_*',
    'keep *_patJetsCa15CHS*_*_*',
    'keep *_NjettinessAk8CHS_*_*',
    'keep *_NjettinessAk8Puppi_*_*',
    'keep *_NjettinessCa15CHS_*_*',
    'keep *_NjettinessCa15SoftDropCHS_*_*',
    "keep *_patJetsCmsTopTagCHSPacked_*_*",
    "keep *_patJetsCmsTopTagCHSSubjets_*_*",
    "keep *_patJetsHepTopTagCHSPacked_*_*",
    "keep *_patJetsHepTopTagCHSSubjets_*_*",
    "keep *_patJetsAk8CHSJetsSoftDropPacked_*_*",
    "keep *_patJetsAk8CHSJetsSoftDropSubjets_*_*",
    "keep *_patJetsAk8PuppiJetsSoftDropPacked_*_*",
    "keep *_patJetsAk8PuppiJetsSoftDropSubjets_*_*",
    "keep *_patJetsCa15CHSJetsSoftDropPacked_*_*",
    "keep *_patJetsCa15CHSJetsSoftDropSubjets_*_*",
    "keep *_patJetsAk8CHSJetsPrunedPacked_*_*",
    "keep *_patJetsAk8CHSJetsPrunedSubjets_*_*",
    "keep *_prunedPrunedGenParticles_*_*",
    "keep *_egmGsfElectronIDs_*_*"
])

###############################################
# RECO AND GEN SETUP
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
#see https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions for latest global tags
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
if useData:
    process.GlobalTag.globaltag = '80X_dataRun2_2016SeptRepro_v5' 
else:
    process.GlobalTag.globaltag = '80X_mcRun2_asymptotic_2016_TrancheIV_v6' 


from RecoJets.Configuration.RecoPFJets_cff import *
from RecoJets.JetProducers.fixedGridRhoProducerFastjet_cfi import *

process.fixedGridRhoFastjetAll = fixedGridRhoFastjetAll.clone(pfCandidatesTag = 'packedPFCandidates')



###############################################
# GEN PARTICLES
#
# The 13TeV samples mainly use Pythia8 for showering, which stores information in another way compared to Pythia6; in particular,
# many intermediate particles are stored such as top quarks or W bosons, which are not required for the analyses and makle the code more complicated.
# Therefore, the 'prunedGenParticles' collection is pruned again; see UHH2/core/python/testgenparticles.py for a test for this pruning
# and more comments.

process.prunedTmp = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("prunedGenParticles"),
    select = cms.vstring(
        'drop *',
        'keep status == 3',
        'keep 20 <= status <= 30',
        'keep 11 <= abs(pdgId)  <= 16 && numberOfMothers()==1 && abs(mother().pdgId()) >= 23 && abs(mother().pdgId()) <= 25',
        'keep 11 <= abs(pdgId)  <= 16 && numberOfMothers()==1 && abs(mother().pdgId()) == 6',
        'keep 11 <= abs(pdgId)  <= 16 && numberOfMothers()==1 && abs(mother().pdgId()) == 42'
    )
)

process.prunedPrunedGenParticles = cms.EDProducer("GenParticlePruner",
    src = cms.InputTag("prunedTmp"),
    select = cms.vstring(
#process.BadChargedCandidateFilter.PFCandidates = cms.InputTag("packedPFCandidates")


### NtupleWriter


isreHLT = False
for x in process.source.fileNames:
    if "reHLT" in x:
        isreHLT = True

triggerpath="HLT"
if isreHLT:
    triggerpath="HLT2"

if useData:
    metfilterpath="RECO"
else:
    metfilterpath="PAT"

process.MyNtuple = cms.EDFilter('NtupleWriter',
        #AnalysisModule = cms.PSet(
        #    name = cms.string("NoopAnalysisModule"),
        #    library = cms.string("libUHH2examples.so"),
        #    # Note: all other settings of type string are passed to the module, e.g.:
        #    TestKey = cms.string("TestValue")
        #),
        fileName = cms.string("Ntuple.root"), 
        doPV = cms.bool(True),
        pv_sources = cms.vstring("offlineSlimmedPrimaryVertices"),
        doRho = cms.untracked.bool(True),
        rho_source = cms.InputTag("fixedGridRhoFastjetAll"),

        save_lepton_keys = cms.bool(True),

        doElectrons = cms.bool(True),
        #doElectrons = cms.bool(False),
        electron_source = cms.InputTag("slimmedElectronsUSER"),
        electron_IDtags = cms.vstring(
          # keys to be stored in UHH2 Electron class via the tag mechanism:
          # each string should correspond to a variable saved
          # via the "userInt" method in the pat::Electron collection used 'electron_source'
          # [the configuration of the pat::Electron::userInt variables should be done in PATElectronUserData]
          'cutBasedElectronID_Summer16_80X_V1_veto',
          'cutBasedElectronID_Summer16_80X_V1_loose',
          'cutBasedElectronID_Summer16_80X_V1_medium',
          'cutBasedElectronID_Summer16_80X_V1_tight',
          'cutBasedElectronHLTPreselection_Summer16_V1',
          'heepElectronID_HEEPV60',
        ),
        #Add variables to trace possible issues with the ECAL slew rate mitigation 
        #https://twiki.cern.ch/twiki/bin/view/CMSPublic/ReMiniAOD03Feb2017Notes#EGM
        doEleAddVars = cms.bool(useData),
        dupECALClusters_source = cms.InputTag('particleFlowEGammaGSFixed:dupECALClusters'),
        hitsNotReplaced_source = cms.InputTag('ecalMultiAndGSGlobalRecHitEB:hitsNotReplaced'),

        doMuons = cms.bool(True),
        muon_sources = cms.vstring("slimmedMuonsUSER"),
        doTaus = cms.bool(True),
        tau_sources = cms.vstring("slimmedTaus" ),
        tau_ptmin = cms.double(0.0),
        tau_etamax = cms.double(999.0),
        doPhotons = cms.bool(False),
        #photon_sources = cms.vstring("selectedPatPhotons"),
        
        doJets = cms.bool(True),
        #jet_sources = cms.vstring("patJetsAk4PFCHS", "patJetsAk8PFCHS", "patJetsCa15CHSJets", "patJetsCa8CHSJets", "patJetsCa15PuppiJets", "patJetsCa8PuppiJets"),
   #     jet_sources = cms.vstring("slimmedJets","slimmedJetsPuppi"),
        jet_sources = cms.vstring("slimmedJets","slimmedJetsPuppi","patJetsAK8PFPUPPI","patJetsAK8PFCHS"),
        jet_ptmin = cms.double(10.0),
        jet_etamax = cms.double(999.0),
        
        doMET = cms.bool(True),
        #met_sources =  cms.vstring("slimmedMETs","slimmedMETsPuppi","slMETsCHS","slimmedMETsMuEGClean"),
        met_sources =  met_sources_GL,
        #doTopJets = cms.bool(False),
        doTopJets = cms.bool(True),
        topjet_ptmin = cms.double(150.0),
        topjet_etamax = cms.double(5.0),                                                                               
        topjet_sources = cms.vstring("slimmedJetsAK8","patJetsAk8CHSJetsSoftDropPacked","patJetsHepTopTagCHSPacked","patJetsHepTopTagPuppiPacked","patJetsAk8PuppiJetsSoftDropPacked"),
      #  topjet_sources = cms.vstring("slimmedJetsAK8","patJetsAk8CHSJetsSoftDropPacked","patJetsAk8PuppiJetsSoftDropPacked"),
        #Note: use label "daughters" for  subjet_sources if you want to store as subjets the linked daughters of the topjets (NOT for slimmedJetsAK8 in miniAOD!)
        #to store a subjet collection present in miniAOD indicate the proper label of the subjets method in pat::Jet: SoftDrop or CMSTopTag
        subjet_sources = cms.vstring("SoftDrop","daughters","daughters","daughters","daughters"),
        #Specify "store" if you want to store b-tagging taginfos for subjet collection, make sure to have included them with .addTagInfos = True
        #addTagInfos = True is currently true by default, however, only for collections produced and not read directly from miniAOD
        #If you don't want to store stubjet taginfos leave string empy ""
        subjet_taginfos = cms.vstring("","store","store","store","store"),
        #Note: if you want to store the MVA Higgs tagger discriminator, specify the jet collection from which to pick it up and the tagger name
        #currently the discriminator is trained on ungroomed jets, so the discriminaotr has to be taken from ungroomed jets
        higgstag_sources = cms.vstring("patJetsAk8CHSJets","patJetsAk8CHSJets","patJetsCa15CHSJets","patJetsCa15PuppiJets","patJetsAk8PuppiJetsFat"),
#        higgstag_sources = cms.vstring("patJetsAK8PFCHS","patJetsAK8PFCHS","patJetsCa15CHSJets","patJetsCa15PuppiJets","patJetsAk8PuppiJetsFat"), #TEST
        higgstag_names = cms.vstring("pfBoostedDoubleSecondaryVertexAK8BJetTags","pfBoostedDoubleSecondaryVertexAK8BJetTags","pfBoostedDoubleSecondaryVertexCA15BJetTags","pfBoostedDoubleSecondaryVertexCA15BJetTags","pfBoostedDoubleSecondaryVertexAK8BJetTags"),
        #Note: if empty, njettiness is directly taken from MINIAOD UserFloat and added to jets, otherwise taken from the provided source (for Run II CMSSW_74 ntuples)
        topjet_njettiness_sources = cms.vstring("","NjettinessAk8CHS","NjettinessCa15CHS","NjettinessCa15Puppi","NjettinessAk8Puppi"),
        topjet_substructure_variables_sources = cms.vstring("","ak8CHSJets","ca15CHSJets", "ca15PuppiJets", "ak8PuppiJetsFat"),
        topjet_njettiness_groomed_sources = cms.vstring("","NjettinessAk8SoftDropCHS","NjettinessCa15SoftDropCHS","NjettinessCa15SoftDropPuppi","NjettinessAk8SoftDropPuppi"),
        topjet_substructure_groomed_variables_sources = cms.vstring("","ak8CHSJetsSoftDropforsub","ca15CHSJetsSoftDropforsub", "ca15PuppiJetsSoftDropforsub", "ak8PuppiJetsSoftDropforsub"),
        #Note: for slimmedJetsAK8 on miniAOD, the pruned mass is available as user flot, with label ak8PFJetsCHSPrunedMass.
        #Alternatively it is possible to specify another pruned jet collection (to be produced here), from which to get it by jet-matching.
        #Finally, it is also possible to leave the pruned mass empty with ""
        topjet_prunedmass_sources = cms.vstring("ak8PFJetsCHSPrunedMass","patJetsAk8CHSJetsPrunedPacked","patJetsCa15CHSJetsPrunedPacked","patJetsCa15CHSJetsPrunedPacked","patJetsAk8CHSJetsPrunedPacked"),
        topjet_softdropmass_sources = cms.vstring("ak8PFJetsCHSSoftDropMass", "", "", "", ""),
        #topjet_sources = cms.vstring("patJetsHepTopTagCHSPacked", "patJetsCmsTopTagCHSPacked", "patJetsCa8CHSJetsPrunedPacked", "patJetsCa15CHSJetsFilteredPacked",
        #        "patJetsHepTopTagPuppiPacked", "patJetsCmsTopTagPuppiPacked", "patJetsCa8PuppiJetsPrunedPacked", "patJetsCa15PuppiJetsFilteredPacked",
        #        'patJetsCa8CHSJetsSoftDropPacked', 'patJetsCa8PuppiJetsSoftDropPacked'
        #        ),
        # jets to match to the topjets in order to get njettiness, in the same order as topjet_sources.
        # Note that no substructure variables are added for the softdrop jets.
        #topjet_substructure_variables_sources = cms.vstring("patJetsCa15CHSJets", "patJetsCa8CHSJets", "patJetsCa8CHSJets", "patJetsCa15CHSJets",
        #        "patJetsCa15PuppiJets", "patJetsCa8PuppiJets", "patJetsCa8PuppiJets", "patJetsCa15PuppiJets",
        #        "patJetsCa8CHSJets", "patJetsCa8PuppiJets"),
        #topjet_njettiness_sources = cms.vstring("NjettinessCa15CHS", "NjettinessCa8CHS", "NjettinessCa8CHS", "NjettinessCa15CHS",
        #        "NjettinessCa15Puppi", "NjettinessCa8Puppi", "NjettinessCa8Puppi", "NjettinessCa15Puppi",
        #        "NjettinessCa8CHS", "NjettinessCa8Puppi"),

        # switch off qjets for now, as it takes a long time:
        #topjet_qjets_sources = cms.vstring("QJetsCa15CHS", "QJetsCa8CHS", "QJetsCa8CHS", "QJetsCa15CHS"),
        
        doTrigger = cms.bool(True), 
        trigger_bits = cms.InputTag("TriggerResults","",triggerpath),
        # MET filters (HBHE noise, CSC, etc.) are stored as trigger Bits in MINIAOD produced in path "PAT"/"RECO" with prefix "Flag_"
        metfilter_bits = cms.InputTag("TriggerResults","",metfilterpath),
        # for now, save all the triggers:
        trigger_prefixes = cms.vstring("HLT_","Flag_"),

        # Give the names of filters for that you want to store the trigger objects that have fired the respecitve trigger
        # filter paths for a given trigger can be found in https://cmsweb.cern.ch/confdb/
        # Example: for HLT_Mu45_eta2p1 the last trigger filter is hltL3fL1sMu16orMu25L1f0L2f10QL3Filtered45e2p1Q
        #          for HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50: relevant filters are hltEle35CaloIdVTGsfTrkIdTGsfDphiFilter (last electron filter), hltEle35CaloIdVTGsfTrkIdTDiCentralPFJet50EleCleaned and hltEle35CaloIdVTGsfTrkIdTCentralPFJet150EleCleaned (for the two jets). 
        #          The  filter hltEle35CaloIdVTGsfTrkIdTCentralPFJet150EleCleaned only included redundant objects that are already included in hltEle35CaloIdVTGsfTrkIdTCentralPFJet50EleCleaned.
        #          for HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50: relevant filters are hltEle45CaloIdVTGsfTrkIdTGsfDphiFilter (last electron filter), hltEle45CaloIdVTGsfTrkIdTDiCentralPFJet50EleCleaned
        triggerObjects_sources = cms.vstring(""),
        #  'hltL3fL1sMu16orMu25L1f0L2f10QL3Filtered45e2p1Q',        # HLT_Mu45_eta2p1_v*
        #  'hltEle35CaloIdVTGsfTrkIdTGsfDphiFilter',                # HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50_v* (electron)
        #  'hltEle35CaloIdVTGsfTrkIdTDiCentralPFJet50EleCleaned',   # HLT_Ele35_CaloIdVT_GsfTrkIdT_PFJet150_PFJet50_v* (jets)
        #  'hltEle45CaloIdVTGsfTrkIdTGsfDphiFilter',                # HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v* (electron)
        #  'hltEle45CaloIdVTGsfTrkIdTDiCentralPFJet50EleCleaned',   # HLT_Ele45_CaloIdVT_GsfTrkIdT_PFJet200_PFJet50_v* (jets)
        #  'hltL3crIsoL1sMu25L1f0L2f10QL3f27QL3trkIsoFiltered0p09', # HLT_IsoMu27_v*
        #  'hltEle27WPLooseGsfTrackIsoFilter',                      # HLT_Ele27_eta2p1_WPLoose_Gsf_v*
        #),
        trigger_objects = cms.InputTag("selectedPatTrigger"),


        
        # *** gen stuff:
        doGenInfo = cms.bool(not useData),
        genparticle_source = cms.InputTag("prunedPrunedGenParticles"),
        stablegenparticle_source = cms.InputTag("packedGenParticles"),
        doAllGenParticles = cms.bool(False), #set to true if you want to store all gen particles, otherwise, only prunedPrunedGenParticles are stored (see above)
        doGenJets = cms.bool(not useData),
        genjet_sources = cms.vstring("slimmedGenJets","slimmedGenJetsAK8","ca15GenJets"),
        genjet_ptmin = cms.double(10.0),
        genjet_etamax = cms.double(5.0),
                            
        doGenTopJets = cms.bool(not useData),

        gentopjet_sources = cms.VInputTag(cms.InputTag("ak8GenJetsSoftDrop")),
#        gentopjet_sources = cms.VInputTag(cms.InputTag("ak8GenJets"),cms.InputTag("ak8GenJetsSoftDrop")), #this can be used to save N-subjettiness for ungroomed GenJets
#        gentopjet_sources = cms.vstring("ak8GenJets","ak8GenJetsSoftDrop"), #irene 
        gentopjet_ptmin = cms.double(150.0), 
        gentopjet_etamax = cms.double(5.0),
        gentopjet_tau1 = cms.VInputTag(),
        gentopjet_tau2 = cms.VInputTag(),
        gentopjet_tau3 = cms.VInputTag(),
#        gentopjet_tau1 = cms.VInputTag(cms.InputTag("NjettinessAk8Gen","tau1"),cms.InputTag("NjettinessAk8SoftDropGen","tau1")), #this can be used to save N-subjettiness for GenJets
#        gentopjet_tau2 = cms.VInputTag(cms.InputTag("NjettinessAk8Gen","tau2"),cms.InputTag("NjettinessAk8SoftDropGen","tau2")), #this can be used to save N-subjettiness for GenJets
#        gentopjet_tau3 = cms.VInputTag(cms.InputTag("NjettinessAk8Gen","tau3"),cms.InputTag("NjettinessAk8SoftDropGen","tau3")), #this can be used to save N-subjettiness for GenJets
        
        doGenJetsWithParts = cms.bool(False),
        doAllPFParticles = cms.bool(False),
        pf_collection_source = cms.InputTag("packedPFCandidates"),

        # # *** HOTVR & XCone stuff
        doHOTVR = cms.bool(True),
        doXCone = cms.bool(True),
        doGenHOTVR = cms.bool(not useData),
        doGenXCone = cms.bool(not useData),    
         # doHOTVR = cms.bool(False),
         # doXCone = cms.bool(False),
         # doGenHOTVR = cms.bool(False),
         # doGenXCone =  cms.bool(False),

)

#process.content = cms.EDAnalyzer("EventContentAnalyzer")

#process.load("FWCore.MessageLogger.MessageLogger_cfi")
#process.MessageLogger = cms.Service("MessageLogger")



# Note: we run in unscheduled mode, i.e. all modules are run as required; just make sure that MyNtuple runs:


process.p = cms.Path(
 #   process.BadPFMuonFilter *
  #  process.BadChargedCandidateFilter *
    process.MyNtuple)

open('pydump.py','w').write(process.dumpPython())
