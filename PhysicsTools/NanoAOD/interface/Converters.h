#ifndef PhysicsTools_NanoAOD_MatchingUtils_h
#define PhysicsTools_NanoAOD_MatchingUtils_h

template <typename ValType, typename ColType = void>
struct
Converters {

    struct Identity {
        static ValType convert(ValType x) { return x; }
    };
    struct Size {
        static int convert(ValType x) { return x.size(); }
    };
    struct Max {
        static ColType convert(ValType x)
        {
            ColType v = std::numeric_limits<ColType>::min();
            for (const auto& i : x)
                if (i > v)
                    v = i;
            return v;
        }
    };
    struct Min {
        static ColType convert(ValType x)
        {
            ColType v = std::numeric_limits<ColType>::max();
            for (const auto& i : x)
                if (i < v)
                    v = i;
            return v;
        }
    };
    struct ScalarPtSum {
        static ColType convert(ValType x)
        {
            ColType v = 0;
            for (const auto& i : x)
                v += i.pt();
            return v;
        }
    };
    struct MassSum {
        static ColType convert(ValType x)
        {
            if (x.empty())
                return 0;
            auto v = x[0].p4();
            for (const auto& i : x)
                v += i.p4();
            return v.mass();
        }
    };
    struct PtVectorSum {
        static ColType convert(ValType x)
        {
            if (x.empty())
                return 0;
            auto v = x[0].p4();
            v -= x[0].p4();
            for (const auto& i : x)
                v += i.p4();
            return v.pt();
        }
    };

};

#endif
