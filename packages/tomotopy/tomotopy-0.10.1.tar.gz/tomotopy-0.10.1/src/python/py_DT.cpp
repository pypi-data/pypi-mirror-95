#include "../TopicModel/DT.h"

#include "module.h"
#include "utils.h"

using namespace std;

tomoto::RawDoc::MiscType DT_misc_args(const tomoto::RawDoc::MiscType& o)
{
	tomoto::RawDoc::MiscType ret;
	ret["timepoint"] = getValueFromMiscDefault<uint32_t>("timepoint", o, "`DTModel` needs a `timepoint` value in `int` type.");
	return ret;
}

static int DT_init(TopicModelObject *self, PyObject *args, PyObject *kwargs)
{
	size_t tw = 0, minCnt = 0, minDf = 0, rmTop = 0;
	size_t K = 1, T = 1;
	float alphaVar = 0.1f, etaVar = 0.1f, phiVar = 0.1f;
	float lrA = 0.01f, lrB = 0.1f, lrC = 0.55f;
	size_t seed = random_device{}();
	PyObject* objCorpus = nullptr, *objTransform = nullptr;
	static const char* kwlist[] = { "tw", "min_cf", "min_df", "rm_top", "k", "t",
		"alpha_var", "eta_var", "phi_var", "lr_a", "lr_b", "lr_c",
		"seed", "corpus", "transform", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|nnnnnnffffffnOO", (char**)kwlist, 
		&tw, &minCnt, &minDf, &rmTop, &K, &T,
		&alphaVar, &etaVar, &phiVar, &lrA, &lrB, &lrC,
		&seed, &objCorpus, &objTransform)) return -1;
	try
	{
		tomoto::ITopicModel* inst = tomoto::IDTModel::create((tomoto::TermWeight)tw, K, T,
			alphaVar, etaVar, phiVar, lrA, lrB, lrC,
			0, seed);
		if (!inst) throw runtime_error{ "unknown tw value" };
		self->inst = inst;
		self->isPrepared = false;
		self->minWordCnt = minCnt;
		self->minWordDf = minDf;
		self->removeTopWord = rmTop;
		self->initParams = py::buildPyDict(kwlist,
			tw, minCnt, minDf, rmTop, K, T, alphaVar, etaVar, phiVar,lrA, lrB, lrC, seed
		);
		py::setPyDictItem(self->initParams, "version", getVersion());

		insertCorpus(self, objCorpus, objTransform);
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return -1;
	}
	return 0;
}

static PyObject* DT_addDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords;
	size_t timepoint = 0;
	static const char* kwlist[] = { "words", "timepoint", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|n", (char**)kwlist, &argWords, &timepoint)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		if (self->isPrepared) throw runtime_error{ "cannot add_doc() after train()" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);
		raw.misc["timepoint"] = (uint32_t)timepoint;
		auto ret = inst->addDoc(raw);
		return py::buildPyValue(ret);
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static DocumentObject* DT_makeDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords;
	size_t timepoint = 0;
	static const char* kwlist[] = { "words", "timepoint", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|n", (char**)kwlist, &argWords, &timepoint)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);
		raw.misc["timepoint"] = (uint32_t)timepoint;
		auto doc = inst->makeDoc(raw);
		py::UniqueObj corpus{ PyObject_CallFunctionObjArgs((PyObject*)&UtilsCorpus_type, (PyObject*)self, nullptr) };
		auto* ret = (DocumentObject*)PyObject_CallFunctionObjArgs((PyObject*)&UtilsDocument_type, corpus.get(), nullptr);
		ret->doc = doc.release();
		ret->owner = true;
		return ret;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* DT_getAlpha(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t timepoint;
	static const char* kwlist[] = { "timepoint", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "n", (char**)kwlist, &timepoint)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/

		if (timepoint >= inst->getT()) throw runtime_error{ "`timepoint` must < `DTModel.num_timepoints`" };

		vector<float> alphas;
		for (size_t i = 0; i < inst->getK(); ++i)
		{
			alphas.emplace_back(inst->getAlpha(i, timepoint));
		}
		return py::buildPyValue(alphas);
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* DT_getPhi(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t timepoint, topicId;
	static const char* kwlist[] = { "timepoint", "topic_id", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "nn", (char**)kwlist, &timepoint, &topicId)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/

		return py::buildPyValue(inst->getPhi(topicId, timepoint));
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* DT_getTopicWords(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topicId, timepoint, topN = 10;
	static const char* kwlist[] = { "topic_id", "timepoint", "top_n", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "nn|n", (char**)kwlist, &topicId, &timepoint, &topN)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		if (topicId >= inst->getK()) throw runtime_error{ "must topic_id < k" };
		if (timepoint >= inst->getT()) throw runtime_error{ "must topic_id < t" };
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/
		return py::buildPyValue(inst->getWordsByTopicSorted(topicId + inst->getK() * timepoint, topN));
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* DT_getTopicWordDist(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topicId, timepoint;
	static const char* kwlist[] = { "topic_id", "timepoint", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "nn", (char**)kwlist, &topicId, &timepoint)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		if (topicId >= inst->getK()) throw runtime_error{ "must topic_id < k" };
		if (timepoint >= inst->getT()) throw runtime_error{ "must topic_id < t" };
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/
		return py::buildPyValue(inst->getWidsByTopic(topicId + inst->getK() * timepoint));
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyObject* DT_getCountByTopics(TopicModelObject* self)
{
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/
		auto l = inst->getCountByTopic();

		npy_intp shapes[2] = { (npy_intp)inst->getT(), (npy_intp)inst->getK() };
		PyObject* ret = PyArray_EMPTY(2, shapes, NPY_INT64, 0);
		for (size_t i = 0; i < inst->getT(); ++i)
		{
			memcpy(PyArray_GETPTR2((PyArrayObject*)ret, i, 0), &l[inst->getK() * i], sizeof(uint64_t) * inst->getK());
		}
		return ret;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

DEFINE_LOADER(DT, DT_type);

static PyMethodDef DT_methods[] =
{
	{ "add_doc", (PyCFunction)DT_addDoc, METH_VARARGS | METH_KEYWORDS, DT_add_doc__doc__ },
	{ "make_doc", (PyCFunction)DT_makeDoc, METH_VARARGS | METH_KEYWORDS, DT_make_doc__doc__ },
	{ "get_count_by_topics", (PyCFunction)DT_getCountByTopics, METH_NOARGS, DT_get_count_by_topics__doc__},
	{ "get_alpha", (PyCFunction)DT_getAlpha, METH_VARARGS | METH_KEYWORDS, DT_get_alpha__doc__ },
	{ "get_phi", (PyCFunction)DT_getPhi, METH_VARARGS | METH_KEYWORDS, DT_get_phi__doc__ },
	{ "get_topic_words", (PyCFunction)DT_getTopicWords, METH_VARARGS | METH_KEYWORDS, DT_get_topic_words__doc__ },
	{ "get_topic_word_dist", (PyCFunction)DT_getTopicWordDist, METH_VARARGS | METH_KEYWORDS, DT_get_topic_word_dist__doc__ },
	{ "load", (PyCFunction)DT_load, METH_STATIC | METH_VARARGS | METH_KEYWORDS, LDA_load__doc__ },
	{ nullptr }
};

DEFINE_GETTER(tomoto::IDTModel, DT, getShapeA);
DEFINE_GETTER(tomoto::IDTModel, DT, getShapeB);
DEFINE_GETTER(tomoto::IDTModel, DT, getShapeC);
DEFINE_GETTER(tomoto::IDTModel, DT, getT);
DEFINE_GETTER(tomoto::IDTModel, DT, getNumDocsByT);

DEFINE_SETTER_CHECKED_FLOAT(tomoto::IDTModel, DT, setShapeA, value > 0);
DEFINE_SETTER_CHECKED_FLOAT(tomoto::IDTModel, DT, setShapeB, value >= 0);
DEFINE_SETTER_CHECKED_FLOAT(tomoto::IDTModel, DT, setShapeC, 0.5 < value && value <= 1);

static PyObject* DT_alpha(TopicModelObject* self, void* closure)
{
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IDTModel*>(self->inst);
		npy_intp shapes[2] = { (npy_intp)inst->getT(), (npy_intp)inst->getK() };
		PyObject* ret = PyArray_EMPTY(2, shapes, NPY_FLOAT, 0);
		for (size_t t = 0; t < inst->getT(); ++t)
		{
			for (size_t k = 0; k < inst->getK(); ++k)
			{
				*(float*)PyArray_GETPTR2((PyArrayObject*)ret, t, k) = inst->getAlpha(k, t);
			}
		}
		return ret;
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_Exception, e.what());
		return nullptr;
	}
}

static PyGetSetDef DT_getseters[] = {
	{ (char*)"lr_a", (getter)DT_getShapeA, (setter)DT_setShapeA, DT_lr_a__doc__, nullptr },
	{ (char*)"lr_b", (getter)DT_getShapeB, (setter)DT_setShapeB, DT_lr_b__doc__, nullptr },
	{ (char*)"lr_c", (getter)DT_getShapeC, (setter)DT_setShapeC, DT_lr_c__doc__, nullptr },
	{ (char*)"alpha", (getter)DT_alpha, nullptr, DT_alpha__doc__, nullptr },
	{ (char*)"eta", nullptr, nullptr, DT_eta__doc__, nullptr },
	{ (char*)"num_timepoints", (getter)DT_getT, nullptr, DT_num_timepoints__doc__, nullptr },
	{ (char*)"num_docs_by_timepoint", (getter)DT_getNumDocsByT, nullptr, DT_num_docs_by_timepoint__doc__, nullptr },
	{ nullptr },
};

TopicModelTypeObject DT_type = { {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"tomotopy.DTModel",             /* tp_name */
	sizeof(TopicModelObject), /* tp_basicsize */
	0,                         /* tp_itemsize */
	(destructor)TopicModelObject::dealloc, /* tp_dealloc */
	0,                         /* tp_print */
	0,                         /* tp_getattr */
	0,                         /* tp_setattr */
	0,                         /* tp_reserved */
	0,                         /* tp_repr */
	0,                         /* tp_as_number */
	0,                         /* tp_as_sequence */
	0,                         /* tp_as_mapping */
	0,                         /* tp_hash  */
	0,                         /* tp_call */
	0,                         /* tp_str */
	0,                         /* tp_getattro */
	0,                         /* tp_setattro */
	0,                         /* tp_as_buffer */
	Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,   /* tp_flags */
	DT___init____doc__,           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	DT_methods,             /* tp_methods */
	0,						 /* tp_members */
	DT_getseters,                         /* tp_getset */
	&LDA_type,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)DT_init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
}, DT_misc_args };

PyObject* Document_eta(DocumentObject* self, void* closure)
{
	try
	{
		if (self->corpus->isIndependent()) throw runtime_error{ "doc doesn't has `eta` field!" };
		if (!self->doc) throw runtime_error{ "doc is null!" };
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentDTM<tomoto::TermWeight::one>*>(self->getBoundDoc());
			if (doc) return py::buildPyValue(doc->eta.array().data(), doc->eta.array().data() + doc->eta.array().size());
		} while (0);
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentDTM<tomoto::TermWeight::idf>*>(self->getBoundDoc());
			if (doc) return py::buildPyValue(doc->eta.array().data(), doc->eta.array().data() + doc->eta.array().size());
		} while (0);
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentDTM<tomoto::TermWeight::pmi>*>(self->getBoundDoc());
			if (doc) return py::buildPyValue(doc->eta.array().data(), doc->eta.array().data() + doc->eta.array().size());
		} while (0);
		throw runtime_error{ "doc doesn't has `eta` field!" };
	}
	catch (const bad_exception&)
	{
		return nullptr;
	}
	catch (const exception& e)
	{
		PyErr_SetString(PyExc_AttributeError, e.what());
		return nullptr;
	}
}

DEFINE_DOCUMENT_GETTER(tomoto::DocumentDTM, timepoint, timepoint);
