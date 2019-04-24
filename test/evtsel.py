#!/usr/bin/env python

import os, re, ROOT
import numpy as np

ROOT.gROOT.SetBatch(True)

def configure():
  import argparse

  parser = argparse.ArgumentParser(description='Configurable options for boosted HH->4b event selection')

  parser.add_argument('-v', '--verbose', action='store_true', default=False,
      help='Print info')

  parser_ana = parser.add_argument_group('analyze')
  parser_ana.add_argument('-n', '--maxEvents', type=int, default=100,
      help='The maximum number of events to process')
  parser_ana.add_argument('-f', '--files', type=str, default='BG_narrow_3000',
      required=False,
      help='File listing datasets to run over')

  parser_condor = parser.add_argument_group('condor')
  parser_condor.add_argument('-c', '--condor', action='store_true', default=False,
      help='Submits jobs to condor')
  parser_condor.add_argument('-s', '--site', type=str, default=None,
      help='Job site where to run CONDOR. Choose either cern for fnal')

  args = parser.parse_args()

  if args.condor:
    if args.site == None:
      parser.error('For running condor jobs stie must be specified: Choose -s cern or -s fnal')

  return args




#def bookHists(fout):




def analyze(args):

  import glob

  chain = ROOT.TChain("Events")

  from input import input
  files = input[args.files]
  for f in files:
    chain.Add(f)

  entries = chain.GetEntriesFast()

  fout = ROOT.TFile(args.files+'.root', 'RECREATE')
  #bookHists(fout)
  fout.cd()
  h_cutflow        = ROOT.TH1D('h_cutflow', 'h_cutflow', 10, 0.5, 10.5)
  h_cutflow.GetXaxis().SetBinLabel(1,"All") ;
  h_cutflow.GetXaxis().SetBinLabel(2,"Trig+N(AK8) #ge 2") ;
  h_cutflow.GetXaxis().SetBinLabel(3 ,"p_{T}+#eta") ; 
  h_cutflow.GetXaxis().SetBinLabel(4,"|#Delta#eta(J_{0}, J_{1}|)") ;
  h_cutflow.GetXaxis().SetBinLabel(5,"#tau_{21}") ; 
  h_cutflow.GetXaxis().SetBinLabel(6,"M(jets)") ;
  h_cutflow.GetXaxis().SetBinLabel(7,"m_{JJ,red}") ; 
  h_cutflow.GetXaxis().SetBinLabel(8,"LL") ;
  h_cutflow.GetXaxis().SetBinLabel(9,"TT") ;

  h_pt_J0          = ROOT.TH1D('h_pt_J0'          , ';p_{T}(J_{0}) [GeV];Events/ 10 GeV;'        ,200 ,0.  , 2000.)
  h_pt_J1          = ROOT.TH1D('h_pt_J1'          , ';(J_T}(J_{1}) [GeV];Events/ 10 GeV;'        ,200 ,0.  , 2000.)
  h_eta_J0         = ROOT.TH1D('h_eta_J0'         , ';#eta(J_{0}) [GeV];Events/ 0.15;'           ,40  ,-3. , 3.   )
  h_eta_J1         = ROOT.TH1D('h_eta_J1'         , ';#eta(J_{1}) [GeV];Events/ 0.15;'           ,40  ,-3. , 3.   )
  h_msoftdrop_J0   = ROOT.TH1D('h_msoftdrop_J0'   , ';m(J_{0}) [GeV];Events/ 10 GeV;'            ,20  ,0.  , 200. )
  h_msoftdrop_J1   = ROOT.TH1D('h_msoftdrop_J1'   , ';m(J_{1}) [GeV];Events/ 10 GeV;'            ,20  ,0.  , 200. )
  h_tau21_J0       = ROOT.TH1D('h_tau21_J0'       , ';#tau_{21}(J_{0});Events/0.05;'             ,20  ,0   , 1.   )
  h_tau21_J1       = ROOT.TH1D('h_tau21_J1'       , ';#tau_{21}(J_{1});Events/0.05;'             ,20  ,0   , 1.   )
  h_doubleb_J0     = ROOT.TH1D('h_doubleb_J0'     , ';Double-b disc.(J_{0});Events/0.1;'         ,20  ,-1. , 1.   )
  h_doubleb_J1     = ROOT.TH1D('h_doubleb_J1'     , ';Double-b disc.(J_{1});Events/0.1;'         ,40  ,-1. , 1.   )
  h_deta_J0J1      = ROOT.TH1D('h_deta_J0J1'      , ';|#Delta#eta(J_{0}, J_{1})|;Events/0.05;'   ,40  ,0   , 2.   )
  h_mjjred_J0J1    = ROOT.TH1D('h_mjjred_J0J1'    , ';m_{JJ,red};Events/20 GeV;'                 ,200 ,0   , 4000.)

  xbins = np.asarray([40, 60, 80, 100, 120, 140, 160, 180, 200, 220], 'f')
  ybins = np.asarray([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, \
      1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 2900, 3000], 'f')
  
  #h2_mjjred_mJ0_SRTT = ROOT.TH2D('h2_mjjred_mJ0_SRTT' ,';;;' ,xbins.size-1, xbins, ybins.size-1, ybins) 
  #h2_mjjred_mJ0_SRLL = ROOT.TH2D('h2_mjjred_mJ0_SRLL' ,';;;' ,xbins.size-1, xbins, ybins.size-1, ybins) 
  #h2_mjjred_mJ0_ATTT = ROOT.TH2D('h2_mjjred_mJ0_ATTT' ,';;;' ,xbins.size-1, xbins, ybins.size-1, ybins) 
  #h2_mjjred_mJ0_ATLL = ROOT.TH2D('h2_mjjred_mJ0_ATLL' ,';;;' ,xbins.size-1, xbins, ybins.size-1, ybins) 

  h2_mjjred_mJ0_SRTT = ROOT.TH2D('h2_mjjred_mJ0_SRTT' ,';;;' ,9 ,40 ,220 ,20 ,1000 ,3000) 
  h2_mjjred_mJ0_SRLL = ROOT.TH2D('h2_mjjred_mJ0_SRLL' ,';;;' ,9 ,40 ,220 ,20 ,1000 ,3000) 
  h2_mjjred_mJ0_ATTT = ROOT.TH2D('h2_mjjred_mJ0_ATTT' ,';;;' ,9 ,40 ,220 ,20 ,1000 ,3000) 
  h2_mjjred_mJ0_ATLL = ROOT.TH2D('h2_mjjred_mJ0_ATLL' ,';;;' ,9 ,40 ,220 ,20 ,1000 ,3000) 

  if args.verbose:
    print('File {chain} has {entries} events'.format(**locals()))
  ievt = 0
  for evt in chain:
    ievt += 1
    if args.maxEvents> 0 and ievt > args.maxEvents: 
      break
    nFatJet = evt.nFatJet
    FatJet_pt = evt.FatJet_pt
    FatJet_eta = evt.FatJet_eta
    FatJet_phi = evt.FatJet_phi
    FatJet_mass = evt.FatJet_mass
    FatJet_msoftdrop = evt.FatJet_msoftdrop
    FatJet_tau2 = evt.FatJet_tau2
    FatJet_tau1 = evt.FatJet_tau1
    #FatJet_deepTagMD_HbbvsQCD = evt.FatJet_deepTagMD_HbbvsQCD
    FatJet_btagHbb = evt.FatJet_btagHbb
    FatJet_jetId = evt.FatJet_jetId
    if args.verbose:
      print('Processing {ievt} have njets = {nFatJet}'.format(**locals()))

    ### Evt sel:
    h_cutflow.Fill(1)

    if nFatJet < 2: 
      continue

    ### Trigger
    if 'Data' in args.files: 
      isData = True
    else:
      isData = False
    if isData:
      isTriggered = evt.HLT_PFHT1050 \
          or evt.HLT_AK8PFHT900_TrimMass50 \
          or evt.HLT_AK8PFJet420_TrimMass30 \
          or evt.HLT_AK8PFJet500 
    else:
      isTriggered = evt.HLT_PFHT780 \
          or evt.HLT_AK8PFHT750_TrimMass50 \
          or evt.HLT_AK8PFJet360_TrimMass30 \
          or evt.HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17 

    if not isTriggered: 
      continue
    h_cutflow.Fill(2)

    idtight_jet0 = evt.FatJet_jetId[0]
    idtight_jet1 = evt.FatJet_jetId[1]

    isAK8Pt = FatJet_pt[0] > 300. and FatJet_pt[1] > 300.
    isAK8Eta = abs(FatJet_eta[0]) < 2.4 and abs(FatJet_eta[1]) < 2.4

    if not (idtight_jet0 > 1 and idtight_jet1 > 1 and isAK8Pt and isAK8Eta):
      continue
    h_cutflow.Fill(3)

    ak8deta = abs(FatJet_eta[0] - FatJet_eta[1])
    isAK8DEta = ak8deta < 1.3 ###4

    t21_jet0 = FatJet_tau2[0]/ FatJet_tau1[0]
    t21_jet1 = FatJet_tau2[1]/ FatJet_tau1[1]
    isAK8t21 = t21_jet0 < 0.45 and t21_jet1 < 0.45 ###5

    mJ0 = FatJet_msoftdrop[0]
    mJ1 = FatJet_msoftdrop[1]
    isAK8Mass_J0 = 105 < mJ0 < 135
    isAK8Mass_J1 = 105 < mJ1 < 135
    isAK8Mass = isAK8Mass_J0 and isAK8Mass_J1

    p4_jet0, p4_jet1 = ROOT.TLorentzVector(), ROOT.TLorentzVector()
    p4_jet0.SetPtEtaPhiM(FatJet_pt[0], FatJet_eta[0], FatJet_phi[0], FatJet_mass[0])
    p4_jet1.SetPtEtaPhiM(FatJet_pt[1], FatJet_eta[1], FatJet_phi[1], FatJet_mass[1])
    mjj = (p4_jet0 + p4_jet1).Mag()
    mjjred = mjj - FatJet_mass[0] - FatJet_mass[1] + 250
    isAK8Mjj = mjjred > 750. ###6

    isSRTT = FatJet_btagHbb[0] > 0.8 and FatJet_btagHbb[1] > 0.8 ###8

    isSRLL = FatJet_btagHbb[0] > 0.3 and FatJet_btagHbb[1] > 0.3 and not isSRTT ###9

    isATTT = FatJet_btagHbb[0] < 0.3 and FatJet_btagHbb[1] > 0.8

    isATLL = FatJet_btagHbb[0] < 0.3 and FatJet_btagHbb[1] > 0.3 and FatJet_btagHbb[1] <= 0.8

    if isAK8Pt and isAK8Eta and isAK8DEta and isAK8t21 and isAK8Mjj and isAK8Mass_J1:
      if isSRTT:
        h2_mjjred_mJ0_SRTT.Fill(mJ0, mjjred)
      if isSRLL:
        h2_mjjred_mJ0_SRLL.Fill(mJ0, mjjred)
      if isATTT:
        h2_mjjred_mJ0_ATTT.Fill(mJ0, mjjred)
      if isATLL:
        h2_mjjred_mJ0_ATLL.Fill(mJ0, mjjred)

    if isAK8DEta: 
      h_cutflow.Fill(4)
      if isAK8t21:
        h_cutflow.Fill(5)
        if isAK8Mass:
          h_cutflow.Fill(6)
          if isAK8Mjj:
            h_cutflow.Fill(7)
            if isSRLL:
              h_cutflow.Fill(8)
            if isSRTT:
              h_cutflow.Fill(9)

    if isAK8Mjj and isAK8Mass and isAK8t21:
      h_deta_J0J1.Fill(ak8deta)

    if isAK8DEta and isAK8Mjj and isAK8Mass:
      h_tau21_J0.Fill(t21_jet0)
      h_tau21_J1.Fill(t21_jet1)

    if isAK8DEta and isAK8Mjj and isAK8t21:
      h_msoftdrop_J0.Fill(FatJet_msoftdrop[0])
      h_msoftdrop_J1.Fill(FatJet_msoftdrop[1])

    if isAK8DEta and isAK8Mass and isAK8t21:
      h_mjjred_J0J1.Fill(mjjred)

    if isAK8DEta and isAK8Mjj:
      h_pt_J0.Fill(FatJet_pt[0])
      h_pt_J1.Fill(FatJet_pt[1])
      h_eta_J0.Fill(FatJet_eta[0])
      h_eta_J1.Fill(FatJet_eta[1])

    if isAK8DEta and isAK8Mass and isAK8t21 and isAK8Mjj:
      h_doubleb_J0.Fill(FatJet_btagHbb[0])
      h_doubleb_J1.Fill(FatJet_btagHbb[1])

    if args.verbose:
      print('isAK8Pt={isAK8Pt} isAK8Eta={isAK8Eta} isAK8DEta={isAK8DEta} isAK8Mjj={isAK8Mjj} isAK8t21={isAK8t21}'.format(**locals()))

  fout.Write()
  fout.Close()

  return




def condor_sub(args, **kwargs):
  workdir = os.getcwd()
  JOB = 'job_{0}'.format(args.files)

  bashscript = open(os.path.join(workdir, JOB+'.sh'), 'w')
  if args.site=='cern':
    from condor_templates import bashscripttemplate_cern as bashscripttemplate
  elif args.site=='fnal':
    from condor_templates import bashscripttemplate_fnal as bashscripttemplate
  bashscriptcontent = bashscripttemplate
  bashscriptcontent = re.sub('JOB', JOB, bashscriptcontent)
  bashscriptcontent = re.sub('GLOBALOPTIONS', '', bashscriptcontent)
  bashscriptcontent = re.sub('NEVT', str(args.maxEvents), bashscriptcontent)
  bashscriptcontent = re.sub('FILES', args.files, bashscriptcontent)
  bashscript.write(bashscriptcontent)
  bashscript.close()

  condor_script = open(os.path.join(workdir, JOB+'.condor'), 'w')
  if args.site=='cern':
    from condor_templates import condor_template_cern as condor_template
  elif args.site=='fnal':
    from condor_templates import condor_template_fnal as condor_template
  condor_script_content = condor_template
  condor_script_content = re.sub('JOB', JOB, condor_template)
  condor_script_content = re.sub('EXEC', JOB+'.sh', condor_script_content)
  if args.site=='cern':
    condor_script_content = re.sub('QUEUE',kwargs['queue'],condor_script_content)
  condor_script.write(condor_script_content)
  condor_script.close()

  return



def main():
  args = configure()

  print(args)

  if args.condor:
    if args.site=='cern':
      kwargs = {'queue': 'longlunch'}
    elif args.site=='fnal':
      kwargs={}
    condor_sub(args, **kwargs)
  else:
    analyze(args)

  return 




if __name__ == "__main__":
  main()
