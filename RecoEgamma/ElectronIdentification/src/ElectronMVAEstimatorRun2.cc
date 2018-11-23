#include "RecoEgamma/ElectronIdentification/interface/ElectronMVAEstimatorRun2.h"

ElectronMVAEstimatorRun2::ElectronMVAEstimatorRun2(const edm::ParameterSet& conf):
  AnyMVAEstimatorRun2Base(conf),
  mvaVarMngr_(conf.getParameter<std::string>("variableDefinition"))
{

  const std::vector <std::string> weightFileNames
    = conf.getParameter<std::vector<std::string> >("weightFileNames");

  const std::vector <std::string> categoryCutStrings
    = conf.getParameter<std::vector<std::string> >("categoryCuts");

  if( (int)(categoryCutStrings.size()) != getNCategories() )
    throw cms::Exception("MVA config failure: ")
      << "wrong number of category cuts in " << getName() << getTag() << std::endl;

  for (int i = 0; i < getNCategories(); ++i) {
      StringCutObjectSelector<reco::GsfElectron> select(categoryCutStrings[i]);
      categoryFunctions_.push_back(select);
  }

  // Initialize GBRForests from weight files
  init(weightFileNames);
}

ElectronMVAEstimatorRun2::ElectronMVAEstimatorRun2( const std::string& mvaTag,
                                                    const std::string& mvaName,
                                                    int nCategories,
                                                    const std::string& variableDefinition,
                                                    const std::vector<std::string>& categoryCutStrings,
                                                    const std::vector<std::string> &weightFileNames,
                                                    bool debug)
  : AnyMVAEstimatorRun2Base( mvaName, mvaTag, nCategories, debug )
  , mvaVarMngr_            (variableDefinition)
{
  
  if( (int)(categoryCutStrings.size()) != getNCategories() )
    throw cms::Exception("MVA config failure: ")
      << "wrong number of category cuts in " << getName() << getTag() << std::endl;
  
  for (int i = 0; i < getNCategories(); ++i) {
    StringCutObjectSelector<reco::GsfElectron> select(categoryCutStrings[i]);
    categoryFunctions_.push_back(select);
  }
  init(weightFileNames);
}



void ElectronMVAEstimatorRun2::init(const std::vector<std::string> &weightFileNames) {

  if(isDebug()) {
    std::cout << " *** Inside " << getName() << getTag() << std::endl;
  }

  // Initialize GBRForests
  if( (int)(weightFileNames.size()) != getNCategories() )
    throw cms::Exception("MVA config failure: ")
      << "wrong number of weightfiles in " << getName() << getTag() << std::endl;

  gbrForests_.clear();
  // Create a TMVA reader object for each category
  for(int i=0; i<getNCategories(); i++){

    std::vector<std::string> variableNamesInCategory;
    std::vector<int> variablesInCategory;

    // Use unique_ptr so that all readers are properly cleaned up
    // when the vector clear() is called in the destructor

    gbrForests_.push_back( GBRForestTools::createGBRForest( weightFileNames[i], variableNamesInCategory ) );

    nVariables_.push_back(variableNamesInCategory.size());

    variables_.push_back(variablesInCategory);

    if(isDebug()) {
      std::cout << " *** Inside " << getName() << getTag() << std::endl;
      std::cout << " category " << i << " with nVariables " << nVariables_[i] << std::endl;
    }

    for (int j=0; j<nVariables_[i];++j) {
        int index = mvaVarMngr_.getVarIndex(variableNamesInCategory[j]);
        if(index == -1) {
            throw cms::Exception("MVA config failure: ")
               << "Concerning " << getName() << getTag() << std::endl
               << "Variable " << variableNamesInCategory[j]
               << " not found in variable definition file!" << std::endl;
        }
        variables_[i].push_back(index);

    }
  }
}

float ElectronMVAEstimatorRun2::
mvaValue( const reco::Candidate* candidate, const std::vector<float>& auxVariables, int &iCategory) const {

  const reco::GsfElectron* electron = dynamic_cast<const reco::GsfElectron*>(candidate);

  if( electron == nullptr ) {
    throw cms::Exception("MVA failure: ")
      << " given particle is expected to be reco::GsfElectron or pat::Electron," << std::endl
      << " but appears to be neither" << std::endl;
  }

  iCategory = findCategory( electron );

  if (iCategory < 0) return -999;

  std::vector<float> vars;

  for (int i = 0; i < nVariables_[iCategory]; ++i) {
      vars.push_back(mvaVarMngr_.getValue(variables_[iCategory][i], electron, auxVariables));
  }

  if(isDebug()) {
    std::cout << " *** Inside " << getName() << getTag() << std::endl;
    std::cout << " category " << iCategory << std::endl;
    for (int i = 0; i < nVariables_[iCategory]; ++i) {
        std::cout << " " << mvaVarMngr_.getName(variables_[iCategory][i]) << " " << vars[i] << std::endl;
    }
  }
  const float response = gbrForests_.at(iCategory)->GetResponse(vars.data()); // The BDT score

  if(isDebug()) {
    std::cout << " ### MVA " << response << std::endl << std::endl;
  }

  return response;
}

int ElectronMVAEstimatorRun2::findCategory( const reco::Candidate* candidate) const {

  const reco::GsfElectron* electron = dynamic_cast<reco::GsfElectron const*>(candidate);

  if( electron == nullptr ) {
    throw cms::Exception("MVA failure: ")
      << " given particle is expected to be reco::GsfElectron or pat::Electron," << std::endl
      << " but appears to be neither" << std::endl;
  }

  return findCategory(electron);

}

int ElectronMVAEstimatorRun2::findCategory( const reco::GsfElectron* electron) const {

  for (int i = 0; i < getNCategories(); ++i) {
      if (categoryFunctions_[i](*electron)) return i;
  }

  edm::LogWarning  ("MVA warning") <<
      "category not defined for particle with pt " << electron->pt() << " GeV, eta " <<
          electron->superCluster()->eta() << " in " << getName() << getTag();

  return -1;

}
