/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__testcell2
#define _nrn_initial _nrn_initial__testcell2
#define nrn_cur _nrn_cur__testcell2
#define _nrn_current _nrn_current__testcell2
#define nrn_jacob _nrn_jacob__testcell2
#define nrn_state _nrn_state__testcell2
#define _net_receive _net_receive__testcell2 
#define rates rates__testcell2 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define e_rev_E _p[0]
#define e_rev_I _p[1]
#define tau_refrac _p[2]
#define v_thresh _p[3]
#define tau_m _p[4]
#define v_rest _p[5]
#define v_reset _p[6]
#define cm _p[7]
#define i_offset _p[8]
#define tau_syn_E _p[9]
#define tau_syn_I _p[10]
#define v_init _p[11]
#define MSEC _p[12]
#define MVOLT _p[13]
#define NFARAD _p[14]
#define i _p[15]
#define copy_v _p[16]
#define iSyn _p[17]
#define regime_refractory _p[18]
#define regime_integrating _p[19]
#define v_I _p[20]
#define lastSpikeTime _p[21]
#define rate_v _p[22]
#define v _p[23]
#define _g _p[24]
#define _tsav _p[25]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_rates();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "rates", _hoc_rates,
 0, 0
};
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "MSEC", "ms",
 "MVOLT", "mV",
 "NFARAD", "microfarads",
 "i", "mA/cm2",
 "copy_v", "mV",
 "iSyn", "nA",
 0,0
};
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 
#define _watch_array _ppvar + 3 
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   Prop* _prop = ((Point_process*)_vptr)->_prop;
   if (_prop) { _nrn_free_watch(_prop->dparam, 3, 3);}
   destroy_point_process(_vptr);
}
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"testcell2",
 "e_rev_E",
 "e_rev_I",
 "tau_refrac",
 "v_thresh",
 "tau_m",
 "v_rest",
 "v_reset",
 "cm",
 "i_offset",
 "tau_syn_E",
 "tau_syn_I",
 "v_init",
 "MSEC",
 "MVOLT",
 "NFARAD",
 0,
 "i",
 "copy_v",
 "iSyn",
 0,
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 26, _prop);
 	/*initialize range parameters*/
 	e_rev_E = -10;
 	e_rev_I = -80;
 	tau_refrac = 5;
 	v_thresh = -50;
 	tau_m = 20;
 	v_rest = -65;
 	v_reset = -65;
 	cm = 1;
 	i_offset = -0.1;
 	tau_syn_E = 2;
 	tau_syn_I = 10;
 	v_init = -65;
 	MSEC = 1;
 	MVOLT = 1;
 	NFARAD = 0.001;
  }
 	_prop->param = _p;
 	_prop->param_size = 26;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 6, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
 
#define _tqitem &(_ppvar[2]._pvoid)
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _testcell2_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 26, 6);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "netsend");
  hoc_register_dparam_semantics(_mechtype, 3, "watch");
  hoc_register_dparam_semantics(_mechtype, 4, "watch");
  hoc_register_dparam_semantics(_mechtype, 5, "watch");
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 testcell2 /Users/padraig/NeuroMLlite/examples/x86_64/testcell2.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Mod file for component: Component(id=testcell2 type=IF_cond_alpha)";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int rates(_threadargsproto_);
 
static double _watch1_cond(_pnt) Point_process* _pnt; {
 	double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
	_thread= (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;
 	_p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
	v = NODEV(_pnt->node);
	return  ( t ) - ( lastSpikeTime + ( tau_refrac * MSEC ) ) ;
}
 
static double _watch2_cond(_pnt) Point_process* _pnt; {
 	double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
	_thread= (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;
 	_p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
	v = NODEV(_pnt->node);
	return  ( v ) - ( v_thresh * MVOLT ) ;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   int _watch_rm = 0;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;  v = NODEV(_pnt->node);
   if (_lflag == 1. ) {*(_tqitem) = 0;}
 {
   if ( _lflag  == 1.0 ) {
       _nrn_watch_activate(_watch_array, _watch1_cond, 1, _pnt, _watch_rm++, 5002.0);
 }
   if ( regime_refractory  == 1.0  && _lflag  == 5002.0 ) {
     regime_refractory = 0.0 ;
     regime_integrating = 1.0 ;
     }
   if ( _lflag  == 1.0 ) {
       _nrn_watch_activate(_watch_array, _watch2_cond, 2, _pnt, _watch_rm++, 5003.0);
 }
   if ( regime_integrating  == 1.0  && _lflag  == 5003.0 ) {
     regime_integrating = 0.0 ;
     regime_refractory = 1.0 ;
     lastSpikeTime = t ;
     v = v_reset * MVOLT ;
     }
   if ( _lflag  == 1.0 ) {
     v = v_init * MVOLT ;
     }
   } 
 NODEV(_pnt->node) = v;
 }
 
static int  rates ( _threadargsproto_ ) {
   iSyn = 0.0 ;
   rate_v = 0.0 + regime_refractory * ( 10000000.0 * ( v_reset * MVOLT - v ) ) + regime_integrating * ( ( MVOLT * ( ( ( i_offset ) / cm ) + ( ( v_rest - ( v / MVOLT ) ) / tau_m ) ) / MSEC ) + ( iSyn / ( cm * NFARAD ) ) ) ;
   v_I = - 1.0 * rate_v ;
    return 0; }
 
static double _hoc_rates(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r = 1.;
 rates ( _p, _ppvar, _thread, _nt );
 return(_r);
}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
 {
   rates ( _threadargs_ ) ;
   rates ( _threadargs_ ) ;
   regime_refractory = 0.0 ;
   regime_integrating = 1.0 ;
   net_send ( _tqitem, (double*)0, _ppvar[1]._pvoid, t +  0.0 , 1.0 ) ;
   }

}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   rates ( _threadargs_ ) ;
   copy_v = v ;
   i = v_I * cm ;
   }
 _current += i;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/padraig/NeuroMLlite/examples/testcell2.mod";
static const char* nmodl_file_text = 
  "TITLE Mod file for component: Component(id=testcell2 type=IF_cond_alpha)\n"
  "\n"
  "COMMENT\n"
  "\n"
  "    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)\n"
  "         org.neuroml.export  v1.7.1\n"
  "         org.neuroml.model   v1.7.1\n"
  "         jLEMS               v0.10.3\n"
  "\n"
  "ENDCOMMENT\n"
  "\n"
  "NEURON {\n"
  "    POINT_PROCESS testcell2\n"
  "    \n"
  "    \n"
  "    NONSPECIFIC_CURRENT i                    : To ensure v of section follows v_I\n"
  "    RANGE e_rev_E                           : parameter\n"
  "    RANGE e_rev_I                           : parameter\n"
  "    RANGE tau_refrac                        : parameter\n"
  "    RANGE v_thresh                          : parameter\n"
  "    RANGE tau_m                             : parameter\n"
  "    RANGE v_rest                            : parameter\n"
  "    RANGE v_reset                           : parameter\n"
  "    RANGE cm                                : parameter\n"
  "    RANGE i_offset                          : parameter\n"
  "    RANGE tau_syn_E                         : parameter\n"
  "    RANGE tau_syn_I                         : parameter\n"
  "    RANGE v_init                            : parameter\n"
  "    RANGE MSEC                              : parameter\n"
  "    RANGE MVOLT                             : parameter\n"
  "    RANGE NFARAD                            : parameter\n"
  "    \n"
  "    RANGE iSyn                              : exposure\n"
  "    \n"
  "    RANGE copy_v                           : copy of v on section\n"
  "    \n"
  "}\n"
  "\n"
  "UNITS {\n"
  "    \n"
  "    (nA) = (nanoamp)\n"
  "    (uA) = (microamp)\n"
  "    (mA) = (milliamp)\n"
  "    (A) = (amp)\n"
  "    (mV) = (millivolt)\n"
  "    (mS) = (millisiemens)\n"
  "    (uS) = (microsiemens)\n"
  "    (molar) = (1/liter)\n"
  "    (kHz) = (kilohertz)\n"
  "    (mM) = (millimolar)\n"
  "    (um) = (micrometer)\n"
  "    (umol) = (micromole)\n"
  "    (S) = (siemens)\n"
  "    \n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "    \n"
  "    e_rev_E = -10 \n"
  "    e_rev_I = -80 \n"
  "    tau_refrac = 5 \n"
  "    v_thresh = -50 \n"
  "    tau_m = 20 \n"
  "    v_rest = -65 \n"
  "    v_reset = -65 \n"
  "    cm = 1 \n"
  "    i_offset = -0.1 \n"
  "    tau_syn_E = 2 \n"
  "    tau_syn_I = 10 \n"
  "    v_init = -65 \n"
  "    MSEC = 1 (ms)\n"
  "    MVOLT = 1 (mV)\n"
  "    NFARAD = 0.001 (microfarads)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "    regime_refractory (1)\n"
  "    regime_integrating (1)\n"
  "    v (mV)\n"
  "    i (mA/cm2)\n"
  "    \n"
  "    copy_v (mV)\n"
  "    \n"
  "    v_I (nA) \n"
  "    lastSpikeTime (ms)                    : Not a state variable as far as Neuron's concerned...\n"
  "    \n"
  "    iSyn (nA)                              : derived variable\n"
  "    \n"
  "    rate_v (mV/ms)\n"
  "    \n"
  "}\n"
  "\n"
  "STATE {\n"
  "    \n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "    rates()\n"
  "    rates() ? To ensure correct initialisation.\n"
  "    \n"
  "    regime_refractory = 0\n"
  "    \n"
  "    regime_integrating = 1\n"
  "    \n"
  "    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state\n"
  "    \n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    \n"
  "    rates()\n"
  "    \n"
  "    copy_v = v\n"
  "    i = v_I * cm\n"
  "}\n"
  "\n"
  "NET_RECEIVE(flag) {\n"
  "    \n"
  "    if (flag == 1) { : Setting watch condition for regime_refractory\n"
  "        WATCH (t >  lastSpikeTime  + (  tau_refrac  *  MSEC  )) 5002\n"
  "    }\n"
  "    \n"
  "    if (regime_refractory == 1 && flag == 5002) { : Setting actions for regime_refractory\n"
  "    \n"
  "            : State assignments\n"
  "    \n"
  "            : Change regime flags\n"
  "            regime_refractory = 0\n"
  "            regime_integrating = 1\n"
  "    \n"
  "            : OnEntry to Regime: integrating (initial = true)\n"
  "    }\n"
  "    \n"
  "    if (flag == 1) { : Setting watch condition for regime_integrating\n"
  "        WATCH (v >  v_thresh  *  MVOLT) 5003\n"
  "    }\n"
  "    \n"
  "    if (regime_integrating == 1 && flag == 5003) { : Setting actions for regime_integrating\n"
  "    \n"
  "            : State assignments\n"
  "    \n"
  "            : Change regime flags\n"
  "            regime_integrating = 0\n"
  "            regime_refractory = 1\n"
  "    \n"
  "            : OnEntry to Regime: refractory (initial = false)\n"
  "    \n"
  "            lastSpikeTime = t\n"
  "    \n"
  "            v = v_reset  *  MVOLT\n"
  "    }\n"
  "    if (flag == 1) { : Set initial states\n"
  "    \n"
  "        v = v_init  *  MVOLT\n"
  "    }\n"
  "    \n"
  "}\n"
  "\n"
  "PROCEDURE rates() {\n"
  "    \n"
  "    ? DerivedVariable is based on path: synapses[*]/i, on: Component(id=testcell2 type=IF_cond_alpha), from synapses; null\n"
  "    iSyn = 0 ? Was: synapses[*]_i but insertion of currents from external attachments not yet supported ? path based, prefix = \n"
  "    \n"
  "    rate_v = 0 + regime_refractory * (10000000 * (v_reset * MVOLT - v)) + regime_integrating * ((  MVOLT   * (((  i_offset  ) /   cm  ) +  ((  v_rest   - (v /   MVOLT  )) /   tau_m  )) /   MSEC  ) + (  iSyn   / (  cm   *   NFARAD  ))) ? Note units of all quantities used here need to be consistent!\n"
  "    \n"
  "    v_I = -1 * rate_v\n"
  "     \n"
  "    \n"
  "}\n"
  "\n"
  ;
#endif
