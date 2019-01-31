#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/NanoAOD/interface/FlatTable.h"
#include "FWCore/Framework/interface/ConsumesCollector.h"
#include "DataFormats/Candidate/interface/Candidate.h"
#include "PhysicsTools/NanoAOD/interface/Converters.h"

#include <utility>
#include <vector>
#include <boost/ptr_container/ptr_vector.hpp>

class GlobalVariablesTableProducer : public edm::stream::EDProducer<> {
    public:

        GlobalVariablesTableProducer( edm::ParameterSet const & params )
            : tablePutToken_(produces<nanoaod::FlatTable>())
        {
            edm::ParameterSet const & varsPSet = params.getParameter<edm::ParameterSet>("variables");
            for (const std::string & vname : varsPSet.getParameterNamesForType<edm::ParameterSet>()) {
                const auto & varPSet = varsPSet.getParameter<edm::ParameterSet>(vname);
                const std::string & type = varPSet.getParameter<std::string>("type");
                if (type == "int") vars_.push_back(new IntVar(vname, nanoaod::FlatTable::IntColumn, varPSet, consumesCollector()));
                else if (type == "float") vars_.push_back(new FloatVar(vname, nanoaod::FlatTable::FloatColumn, varPSet, consumesCollector()));
                else if (type == "double") vars_.push_back(new DoubleVar(vname, nanoaod::FlatTable::FloatColumn, varPSet, consumesCollector()));
                else if (type == "bool") vars_.push_back(new BoolVar(vname, nanoaod::FlatTable::UInt8Column, varPSet, consumesCollector()));
                else if (type == "candidatescalarsum") vars_.push_back(new CandidateScalarSumVar(vname, nanoaod::FlatTable::FloatColumn, varPSet, consumesCollector()));
                else if (type == "candidatesize") vars_.push_back(new CandidateSizeVar(vname, nanoaod::FlatTable::IntColumn, varPSet, consumesCollector()));
                else if (type == "candidatesummass") vars_.push_back(new CandidateSumMassVar(vname, nanoaod::FlatTable::FloatColumn, varPSet, consumesCollector()));
                else throw cms::Exception("Configuration", "unsupported type "+type+" for variable "+vname);
            }
        }

        void produce(edm::Event& iEvent, const edm::EventSetup& iSetup) override {
            nanoaod::FlatTable out(1, "", true);

            for (const auto & var : vars_) var.fill(iEvent, out);

            iEvent.emplace(tablePutToken_, std::move(out));
        }

    private:
        class Variable {
            public:
                Variable(const std::string & aname, nanoaod::FlatTable::ColumnType atype, const edm::ParameterSet & cfg) : 
                    name_(aname), doc_(cfg.getParameter<std::string>("doc")), type_(atype) {}
                virtual ~Variable() {}
                virtual void fill(const edm::Event &iEvent, nanoaod::FlatTable & out) const = 0;
                const std::string & name() const { return name_; }
                const nanoaod::FlatTable::ColumnType & type() const { return type_; }
            protected:
                std::string name_, doc_;
                nanoaod::FlatTable::ColumnType type_;
        };

        template<typename ValType, typename ColType=ValType,  typename Converter=typename Converters<ValType>::Identity >
            class VariableT : public Variable {
                public:
                    VariableT(const std::string & aname, nanoaod::FlatTable::ColumnType atype, const edm::ParameterSet & cfg, edm::ConsumesCollector && cc) :
                        Variable(aname, atype, cfg), src_(cc.consumes<ValType>(cfg.getParameter<edm::InputTag>("src"))) {}
                    void fill(const edm::Event &iEvent, nanoaod::FlatTable & out) const override {
                        out.template addColumnValue<ColType>(this->name_, Converter::convert(iEvent.get(src_)), this->doc_, this->type_);
                    }
                protected:
                    edm::EDGetTokenT<ValType> src_;
            };
        typedef VariableT<int> IntVar;
        typedef VariableT<float> FloatVar;
        typedef VariableT<double,float> DoubleVar;
        typedef VariableT<bool,uint8_t> BoolVar;
        typedef VariableT<edm::View<reco::Candidate>,float,Converters<edm::View<reco::Candidate>,float>::ScalarPtSum> CandidateScalarSumVar;
        typedef VariableT<edm::View<reco::Candidate>,float,Converters<edm::View<reco::Candidate>,float>::MassSum> CandidateSumMassVar;
        typedef VariableT<edm::View<reco::Candidate>,int,Converters<edm::View<reco::Candidate>>::Size> CandidateSizeVar;
        boost::ptr_vector<Variable> vars_;

        const std::vector<edm::EDGetToken> srcTokens_;
        const edm::EDPutTokenT<nanoaod::FlatTable> tablePutToken_;
};

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(GlobalVariablesTableProducer);
