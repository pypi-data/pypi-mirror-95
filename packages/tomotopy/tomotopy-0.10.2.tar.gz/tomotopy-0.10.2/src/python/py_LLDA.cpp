#include "../TopicModel/LLDA.h"

#include "module.h"
#include "utils.h"

using namespace std;

tomoto::RawDoc::MiscType LLDA_misc_args(const tomoto::RawDoc::MiscType& o)
{
	tomoto::RawDoc::MiscType ret;
	ret["labels"] = getValueFromMiscDefault<vector<string>>("labels", o, "`LLDAModel` needs a `labels` value in `Iterable[str]` type.");
	return ret;
}

static int LLDA_init(TopicModelObject *self, PyObject *args, PyObject *kwargs)
{
	size_t tw = 0, minCnt = 0, minDf = 0, rmTop = 0;
	size_t K = 1;
	float alpha = 0.1f, eta = 0.01f;
	size_t seed = random_device{}();
	PyObject* objCorpus = nullptr, *objTransform = nullptr;
	static const char* kwlist[] = { "tw", "min_cf", "min_df", "rm_top", "k", "alpha", "eta", 
		"seed", "corpus", "transform", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|nnnnfffnOO", (char**)kwlist, &tw, &minCnt, &minDf, &rmTop,
		&K, &alpha, &eta, &seed, &objCorpus, &objTransform)) return -1;
	try
	{
		tomoto::ITopicModel* inst = tomoto::ILLDAModel::create((tomoto::TermWeight)tw, K, alpha, eta, seed);
		if (!inst) throw runtime_error{ "unknown tw value" };
		self->inst = inst;
		self->isPrepared = false;
		self->minWordCnt = minCnt;
		self->minWordDf = minDf;
		self->removeTopWord = rmTop;
		self->initParams = py::buildPyDict(kwlist,
			tw, minCnt, minDf, rmTop, K, alpha, eta, seed
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

static PyObject* LLDA_addDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords, *argLabels = nullptr;
	static const char* kwlist[] = { "words", "labels", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", (char**)kwlist, &argWords, &argLabels)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		if (self->isPrepared) throw runtime_error{ "cannot add_doc() after train()" };
		auto* inst = static_cast<tomoto::ILLDAModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);
		if(argLabels)
		{
			if (PyUnicode_Check(argLabels)) PRINT_WARN_ONCE("[warn] 'labels' should be an iterable of str.");
			raw.misc["labels"] = py::toCpp<vector<string>>(argLabels, "`labels` must be an iterable of str.");
		}
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

static DocumentObject* LLDA_makeDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords, *argLabels = nullptr;
	static const char* kwlist[] = { "words", "labels", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|O", (char**)kwlist, &argWords, &argLabels)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::ILLDAModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);

		if (argLabels)
		{
			if (PyUnicode_Check(argLabels)) PRINT_WARN_ONCE("[warn] 'labels' should be an iterable of str.");
			raw.misc["labels"] = py::toCpp<vector<string>>(argLabels, "`labels` must be an iterable of str.");
		}
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

static VocabObject* LLDA_getTopicLabelDict(TopicModelObject* self, void* closure)
{
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* ret = (VocabObject*)PyObject_CallObject((PyObject*)&UtilsVocab_type, nullptr);
		ret->dep = (PyObject*)self;
		Py_INCREF(ret->dep);
		ret->vocabs = (tomoto::Dictionary*)&static_cast<tomoto::ILLDAModel*>(self->inst)->getTopicLabelDict();
		ret->size = -1;
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

PyObject* Document_labels(DocumentObject* self, void* closure)
{
	auto makeReturn = [&](const tomoto::DocumentBase* doc, const Eigen::Matrix<int8_t, -1, 1>& labelMask)
	{
		auto inst = dynamic_cast<tomoto::ILLDAModel*>(self->corpus->tm->inst);
		auto dict = inst->getTopicLabelDict();
		vector<pair<string, vector<float>>> ret;
		auto topicDist = inst->getTopicsByDoc(doc);
		for (size_t i = 0; i < dict.size(); ++i)
		{
			if (labelMask[i * inst->getNumTopicsPerLabel()])
			{
				ret.emplace_back(inst->getTopicLabelDict().toWord(i), 
					vector<float>{ &topicDist[i * inst->getNumTopicsPerLabel()], &topicDist[(i + 1) * inst->getNumTopicsPerLabel()] });
			}
		}
		return py::buildPyValue(ret);
	};

	try
	{
		if (self->corpus->isIndependent()) throw runtime_error{ "doc doesn't has `labels` field!" };
		if (!self->doc) throw runtime_error{ "doc is null!" };
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentLLDA<tomoto::TermWeight::one>*>(self->getBoundDoc());
			if (doc) return makeReturn(doc, doc->labelMask);
		} while (0);
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentLLDA<tomoto::TermWeight::idf>*>(self->getBoundDoc());
			if (doc) return makeReturn(doc, doc->labelMask);
		} while (0);
		do
		{
			auto* doc = dynamic_cast<const tomoto::DocumentLLDA<tomoto::TermWeight::pmi>*>(self->getBoundDoc());
			if (doc) return makeReturn(doc, doc->labelMask);
		} while (0);
		throw runtime_error{ "doc doesn't has `labels` field!" };
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

DEFINE_LOADER(LLDA, LLDA_type);

PyObject* LDA_getTopicWords(TopicModelObject* self, PyObject* args, PyObject *kwargs);

static PyMethodDef LLDA_methods[] =
{
	{ "add_doc", (PyCFunction)LLDA_addDoc, METH_VARARGS | METH_KEYWORDS, LLDA_add_doc__doc__ },
	{ "make_doc", (PyCFunction)LLDA_makeDoc, METH_VARARGS | METH_KEYWORDS, LLDA_make_doc__doc__ },
	{ "load", (PyCFunction)LLDA_load, METH_STATIC | METH_VARARGS | METH_KEYWORDS, LDA_load__doc__ },
	{ "get_topic_words", (PyCFunction)LDA_getTopicWords, METH_VARARGS | METH_KEYWORDS, LLDA_get_topic_words__doc__},
	{ nullptr }
};

static PyGetSetDef LLDA_getseters[] = {
	{ (char*)"topic_label_dict", (getter)LLDA_getTopicLabelDict, nullptr, LLDA_topic_label_dict__doc__, nullptr },
	{ nullptr },
};


TopicModelTypeObject LLDA_type = { {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"tomotopy.LLDAModel",             /* tp_name */
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
	LLDA___init____doc__,           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	LLDA_methods,             /* tp_methods */
	0,						 /* tp_members */
	LLDA_getseters,                         /* tp_getset */
	&LDA_type,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)LLDA_init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
}, LLDA_misc_args };
