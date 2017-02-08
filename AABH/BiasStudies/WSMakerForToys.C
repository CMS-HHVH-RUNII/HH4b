void WSMakerForToys(int category){

  cout << "category " << category << endl; 

   // Load the combine Library 
   gSystem->Load("libHiggsAnalysisCombinedLimit.so");

   string sCategory;
   // Open the dummy H->gg workspace 
   if (category == 0) sCategory = string("LL");
   else if (category == 1) sCategory = string("TT");


   TFile *f_bkg = TFile::Open(Form("../outputs/datacards/w_background_%s.root", sCategory.c_str()));

   RooWorkspace *w_bkg = (RooWorkspace*)f_bkg->Get("HH4b;1");


   // w_all:CMS_bkg_fit_CMS_jj_4btag_cat0
   // The observable (CMS_hgg_mass in the workspace)
   RooRealVar *mass =  w_bkg->var("x");

   string file;

   // Get three of the functions inside, exponential, linear polynomial, power law
   RooAbsPdf *pdf_exp_sr = w_bkg->pdf("bg_");
   RooAbsPdf *pdf_exp_sb = w_bkg->pdf("bgSB_");

   // Fit the functions to the data to set the "prefit" state (note this can and should be redone with combine when doing 
   // bias studies as one typically throws toys from the "best-fit"
   //RooDataSet *data = w_hgg->data("roohist_data_mass_cat1_toy1_cutrange__CMS_hgg_mass");
   //pdf_exp->fitTo(*data);  // index 0
   //   pdf_pow->fitTo(*data); // index 1 
   //   pdf_pol->fitTo(*data);   // index 2
   /*
   // Make a plot (data is a toy dataset)

   RooPlot *plot = mass->frame(); //  data->plotOn(plot);
   pdf_exp->plotOn(plot,RooFit::LineColor(kGreen));
   //   pdf_pol->plotOn(plot,RooFit::LineColor(kBlue));
   //  pdf_pow->plotOn(plot,RooFit::LineColor(kRed));
   plot->SetTitle("PDF fits to toy data");
   plot->Draw();

   cout << "Norm = " << pdf_exp->getNorm() << endl;

   // Make a RooCategory object. This will control which of the pdfs is "active"
   RooCategory cat("pdf_index","Index of Pdf which is active");
   */

   RooCategory cat("pdf_index","Index of Pdf which is active");

   // Make a RooMultiPdf object. The order of the pdfs will be the order of their index, ie for below 
   // 0 == exponential
   // 1 == linear function
   // 2 == powerlaw
   RooArgList mypdfs_sr;
   mypdfs_sr.add(*pdf_exp_sr);

   RooArgList mypdfs_sb;
   mypdfs_sb.add(*pdf_exp_sb);




   //  mypdfs.add(*pdf_pol);
   //  mypdfs.add(*pdf_pow);
   
   RooMultiPdf multipdf_sr("roomultipdf_sr","All Pdfs",cat,mypdfs_sr);
   RooMultiPdf multipdf_sb("roomultipdf_sb","All Pdfs",cat,mypdfs_sb);
   
   // As usual make an extended term for the background with _norm for freely floating yield
   RooRealVar norm("roomultipdf_norm","Number of background events",0,100000);
   
   // Save to a new workspace
   TFile *fout = new TFile(Form("workspaces/background_pdfs_cat_%s.root",sCategory.c_str()),"RECREATE");
   RooWorkspace wout_sr("backgrounds_sr","backgrounds_sr");
   wout_sr.import(cat);
   //   wout_sr.import(norm);
   wout_sr.import(multipdf_sr);
   wout_sr.Print();
   wout_sr.Write();

   RooWorkspace wout_sb("backgrounds_sb","backgrounds_sb");
   wout_sb.import(cat);
   //   wout_sb.import(norm);
   wout_sb.import(multipdf_sb);
   wout_sb.Print();
   wout_sb.Write();

   fout->Close();
}
