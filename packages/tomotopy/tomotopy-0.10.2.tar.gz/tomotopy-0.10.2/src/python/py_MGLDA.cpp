#include "../TopicModel/MGLDA.h"

#include "module.h"
#include "utils.h"

using namespace std;

tomoto::RawDoc::MiscType MGLDA_misc_args(const tomoto::RawDoc::MiscType& o)
{
	tomoto::RawDoc::MiscType ret;
	ret["delimiter"] = getValueFromMiscDefault<string>("delimiter", o, "`MGLDAModel` needs a `delimiter` value in `str` type.", ".");
	return ret;
}

static int MGLDA_init(TopicModelObject *self, PyObject *args, PyObject *kwargs)
{
	size_t tw = 0, minCnt = 0, minDf = 0, rmTop = 0;
	size_t K = 1, KL = 1, T = 3;
	float alpha = 0.1f, alphaL = 0.1f, eta = 0.01f, etaL = 0.01f, alphaM = 0.1f, alphaML = 0.1f, gamma = 0.1f;
	size_t seed = random_device{}();
	PyObject* objCorpus = nullptr, *objTransform = nullptr;
	static const char* kwlist[] = { "tw", "min_cf", "min_df", "rm_top", "k_g", "k_l", "t", "alpha_g", "alpha_l", "alpha_mg", "alpha_ml",
		"eta_g", "eta_l", "gamma", "seed", "corpus", "transform", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "|nnnnnnnfffffffnOO", (char**)kwlist, &tw, &minCnt, &minDf, &rmTop,
		&K, &KL, &T, &alpha, &alphaL, &alphaM, &alphaML, &eta, &etaL, &gamma, 
		&seed, &objCorpus, &objTransform)) return -1;
	try
	{
		tomoto::ITopicModel* inst = tomoto::IMGLDAModel::create((tomoto::TermWeight)tw, 
			K, KL, T, alpha, alphaL, alphaM, alphaML, eta, etaL, gamma, seed);
		if (!inst) throw runtime_error{ "unknown tw value" };
		self->inst = inst;
		self->isPrepared = false;
		self->minWordCnt = minCnt;
		self->minWordDf = minDf;
		self->removeTopWord = rmTop;
		self->initParams = py::buildPyDict(kwlist,
			tw, minCnt, minDf, rmTop, K, KL, T, alpha, alphaL, alphaM, alphaML, eta, etaL, gamma, seed
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

static PyObject* MGLDA_addDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords;
	const char* delimiter = ".";
	static const char* kwlist[] = { "words", "delimiter", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|s", (char**)kwlist, &argWords, &delimiter)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		if (self->isPrepared) throw runtime_error{ "cannot add_doc() after train()" };
		auto* inst = static_cast<tomoto::IMGLDAModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);
		raw.misc["delimiter"] = delimiter;
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

static DocumentObject* MGLDA_makeDoc(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	PyObject *argWords;
	const char* delimiter = ".";
	static const char* kwlist[] = { "words", "delimiter", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O|s", (char**)kwlist, &argWords, &delimiter)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IMGLDAModel*>(self->inst);
		if (PyUnicode_Check(argWords)) PRINT_WARN_ONCE("[warn] 'words' should be an iterable of str.");
		tomoto::RawDoc raw = buildRawDoc(argWords);
		raw.misc["delimiter"] = delimiter;
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

static PyObject* MGLDA_getTopicWords(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topicId, topN = 10;
	static const char* kwlist[] = { "topic_id", "top_n", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "n|n", (char**)kwlist, &topicId, &topN)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IMGLDAModel*>(self->inst);
		if (topicId >= inst->getK() + inst->getKL()) throw runtime_error{ "must topic_id < KG + KL" };
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/
		return py::buildPyValue(inst->getWordsByTopicSorted(topicId, topN));
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

static PyObject* MGLDA_getTopicWordDist(TopicModelObject* self, PyObject* args, PyObject *kwargs)
{
	size_t topicId;
	static const char* kwlist[] = { "topic_id", nullptr };
	if (!PyArg_ParseTupleAndKeywords(args, kwargs, "n", (char**)kwlist, &topicId)) return nullptr;
	try
	{
		if (!self->inst) throw runtime_error{ "inst is null" };
		auto* inst = static_cast<tomoto::IMGLDAModel*>(self->inst);
		if (topicId >= inst->getK() + inst->getKL()) throw runtime_error{ "must topic_id < KG + KL" };
		/*if (!self->isPrepared)
		{
			inst->prepare(true, self->minWordCnt, self->minWordDf, self->removeTopWord);
			self->isPrepared = true;
		}*/
		return py::buildPyValue(inst->getWidsByTopic(topicId));
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

DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getKL);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getGamma);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getAlphaL);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getAlphaM);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getAlphaML);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getEtaL);
DEFINE_GETTER(tomoto::IMGLDAModel, MGLDA, getT);

DEFINE_DOCUMENT_GETTER_REORDER(tomoto::DocumentMGLDA, windows, Vs);

DEFINE_LOADER(MGLDA, MGLDA_type);


static PyMethodDef MGLDA_methods[] =
{
	{ "load", (PyCFunction)MGLDA_load, METH_STATIC | METH_VARARGS | METH_KEYWORDS, LDA_load__doc__ },
	{ "add_doc", (PyCFunction)MGLDA_addDoc, METH_VARARGS | METH_KEYWORDS, MGLDA_add_doc__doc__ },
	{ "make_doc", (PyCFunction)MGLDA_makeDoc, METH_VARARGS | METH_KEYWORDS, MGLDA_make_doc__doc__ },
	{ "get_topic_words", (PyCFunction)MGLDA_getTopicWords, METH_VARARGS | METH_KEYWORDS, MGLDA_get_topic_words__doc__ },
	{ "get_topic_word_dist", (PyCFunction)MGLDA_getTopicWordDist, METH_VARARGS | METH_KEYWORDS, MGLDA_get_topic_word_dist__doc__ },
	{ nullptr }
};

static PyGetSetDef MGLDA_getseters[] = {
	{ (char*)"k_g", (getter)LDA_getK, nullptr, MGLDA_k_g__doc__, nullptr },
	{ (char*)"k_l", (getter)MGLDA_getKL, nullptr, MGLDA_k_l__doc__, nullptr },
	{ (char*)"gamma", (getter)MGLDA_getGamma, nullptr, MGLDA_gamma__doc__, nullptr },
	{ (char*)"t", (getter)MGLDA_getT, nullptr, MGLDA_t__doc__, nullptr },
	{ (char*)"alpha_g", (getter)LDA_getAlpha, nullptr, MGLDA_alpha_g__doc__, nullptr },
	{ (char*)"alpha_l", (getter)MGLDA_getAlphaL, nullptr, MGLDA_alpha_l__doc__, nullptr },
	{ (char*)"alpha_mg", (getter)MGLDA_getAlphaM, nullptr, MGLDA_alpha_mg__doc__, nullptr },
	{ (char*)"alpha_ml", (getter)MGLDA_getAlphaML, nullptr, MGLDA_alpha_ml__doc__, nullptr },
	{ (char*)"eta_g", (getter)LDA_getEta, nullptr, MGLDA_eta_g__doc__, nullptr },
	{ (char*)"eta_l", (getter)MGLDA_getEtaL, nullptr, MGLDA_eta_l__doc__, nullptr },
	{ nullptr },
};

TopicModelTypeObject MGLDA_type = { {
	PyVarObject_HEAD_INIT(nullptr, 0)
	"tomotopy.MGLDAModel",             /* tp_name */
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
	MGLDA___init____doc__,           /* tp_doc */
	0,                         /* tp_traverse */
	0,                         /* tp_clear */
	0,                         /* tp_richcompare */
	0,                         /* tp_weaklistoffset */
	0,                         /* tp_iter */
	0,                         /* tp_iternext */
	MGLDA_methods,             /* tp_methods */
	0,						 /* tp_members */
	MGLDA_getseters,                         /* tp_getset */
	&LDA_type,                         /* tp_base */
	0,                         /* tp_dict */
	0,                         /* tp_descr_get */
	0,                         /* tp_descr_set */
	0,                         /* tp_dictoffset */
	(initproc)MGLDA_init,      /* tp_init */
	PyType_GenericAlloc,
	PyType_GenericNew,
}, MGLDA_misc_args };