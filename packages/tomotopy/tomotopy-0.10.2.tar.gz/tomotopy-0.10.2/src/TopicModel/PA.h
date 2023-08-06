#pragma once
#include "LDA.h"

namespace tomoto
{
    template<TermWeight _tw>
	struct DocumentPA : public DocumentLDA<_tw>
	{
		using BaseDocument = DocumentLDA<_tw>;
		using DocumentLDA<_tw>::DocumentLDA;
		using WeightType = typename DocumentLDA<_tw>::WeightType;

		tvector<Tid> Z2s;
		Eigen::Matrix<WeightType, -1, -1> numByTopic1_2;

		template<typename _TopicModel> void update(WeightType* ptr, const _TopicModel& mdl);

		DEFINE_SERIALIZER_AFTER_BASE_WITH_VERSION(BaseDocument, 0, Z2s);
		DEFINE_TAGGED_SERIALIZER_AFTER_BASE_WITH_VERSION(BaseDocument, 1, 0x00010001, Z2s);
	};
    
    class IPAModel : public ILDAModel
	{
	public:
		using DefaultDocType = DocumentPA<TermWeight::one>;
		static IPAModel* create(TermWeight _weight, size_t _K1 = 1, size_t _K2 = 1, 
			Float _alpha = 0.1, Float _eta = 0.01, size_t seed = std::random_device{}(),
			bool scalarRng = false);

		virtual size_t getDirichletEstIteration() const = 0;
		virtual void setDirichletEstIteration(size_t iter) = 0;
		virtual size_t getK2() const = 0;
		virtual Float getSubAlpha(Tid k1, Tid k2) const = 0;
		virtual std::vector<Float> getSubAlpha(Tid k1) const = 0;
		virtual std::vector<Float> getSubTopicBySuperTopic(Tid k) const = 0;
		virtual std::vector<std::pair<Tid, Float>> getSubTopicBySuperTopicSorted(Tid k, size_t topN) const = 0;

		virtual std::vector<Float> getSubTopicsByDoc(const DocumentBase* doc) const = 0;
		virtual std::vector<std::pair<Tid, Float>> getSubTopicsByDocSorted(const DocumentBase* doc, size_t topN) const = 0;

		virtual std::vector<uint64_t> getCountBySuperTopic() const = 0;
	};
}
