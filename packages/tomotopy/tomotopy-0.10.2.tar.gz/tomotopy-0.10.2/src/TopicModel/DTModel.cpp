#include "DTModel.hpp"

namespace tomoto
{
	/*template class DTModel<TermWeight::one>;
	template class DTModel<TermWeight::idf>;
	template class DTModel<TermWeight::pmi>;*/

	IDTModel* IDTModel::create(TermWeight _weight, size_t _K, size_t _T, 
		Float _alphaVar, Float _etaVar, Float _phiVar,
		Float _shapeA, Float _shapeB, Float _shapeC, Float _etaRegL2, size_t seed, bool scalarRng)
	{
		TMT_SWITCH_TW(_weight, scalarRng, DTModel, _K, _T, _alphaVar, _etaVar, _phiVar, _shapeA, _shapeB, _shapeC, _etaRegL2, seed);
	}
}
