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
 
#define nrn_init _nrn_init__poissonFiringSyn100Hz
#define _nrn_initial _nrn_initial__poissonFiringSyn100Hz
#define nrn_cur _nrn_cur__poissonFiringSyn100Hz
#define _nrn_current _nrn_current__poissonFiringSyn100Hz
#define nrn_jacob _nrn_jacob__poissonFiringSyn100Hz
#define nrn_state _nrn_state__poissonFiringSyn100Hz
#define _net_receive _net_receive__poissonFiringSyn100Hz 
#define noiseFromRandom noiseFromRandom__poissonFiringSyn100Hz 
#define rates rates__poissonFiringSyn100Hz 
#define seed seed__poissonFiringSyn100Hz 
#define states states__poissonFiringSyn100Hz 
 
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
#define weight _p[0]
#define averageRate _p[1]
#define averageIsi _p[2]
#define SMALL_TIME _p[3]
#define synInput_tauRise _p[4]
#define synInput_tauDecay _p[5]
#define synInput_peakTime _p[6]
#define synInput_waveformFactor _p[7]
#define synInput_gbase _p[8]
#define synInput_erev _p[9]
#define synInput_g _p[10]
#define synInput_i _p[11]
#define iSyn _p[12]
#define i _p[13]
#define tsince _p[14]
#define tnextIdeal _p[15]
#define tnextUsed _p[16]
#define synInput_A _p[17]
#define synInput_B _p[18]
#define isi _p[19]
#define rate_tsince _p[20]
#define rate_tnextUsed _p[21]
#define rate_tnextIdeal _p[22]
#define rate_synInput_A _p[23]
#define rate_synInput_B _p[24]
#define Dtsince _p[25]
#define DtnextIdeal _p[26]
#define DtnextUsed _p[27]
#define DsynInput_A _p[28]
#define DsynInput_B _p[29]
#define v _p[30]
#define _g _p[31]
#define _tsav _p[32]
#define _nd_area  *_ppvar[0]._pval
#define donotuse	*_ppvar[2]._pval
#define _p_donotuse	_ppvar[2]._pval
 
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
 static int hoc_nrnpointerindex =  2;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_H();
 static double _hoc_erand();
 static double _hoc_noiseFromRandom();
 static double _hoc_random_float();
 static double _hoc_rates();
 static double _hoc_seed();
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
 "H", _hoc_H,
 "erand", _hoc_erand,
 "noiseFromRandom", _hoc_noiseFromRandom,
 "random_float", _hoc_random_float,
 "rates", _hoc_rates,
 "seed", _hoc_seed,
 0, 0
};
#define H H_poissonFiringSyn100Hz
#define erand erand_poissonFiringSyn100Hz
#define random_float random_float_poissonFiringSyn100Hz
 extern double H( _threadargsprotocomma_ double );
 extern double erand( _threadargsproto_ );
 extern double random_float( _threadargsprotocomma_ double );
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "averageRate", "kHz",
 "averageIsi", "ms",
 "SMALL_TIME", "ms",
 "synInput_tauRise", "ms",
 "synInput_tauDecay", "ms",
 "synInput_peakTime", "ms",
 "synInput_gbase", "uS",
 "synInput_erev", "mV",
 "tsince", "ms",
 "tnextIdeal", "ms",
 "tnextUsed", "ms",
 "synInput_g", "uS",
 "synInput_i", "nA",
 "iSyn", "nA",
 "i", "nA",
 0,0
};
 static double delta_t = 0.01;
 static double synInput_B0 = 0;
 static double synInput_A0 = 0;
 static double tnextUsed0 = 0;
 static double tnextIdeal0 = 0;
 static double tsince0 = 0;
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
 
#define _watch_array _ppvar + 4 
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   Prop* _prop = ((Point_process*)_vptr)->_prop;
   if (_prop) { _nrn_free_watch(_prop->dparam, 4, 3);}
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[7]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"poissonFiringSyn100Hz",
 "weight",
 "averageRate",
 "averageIsi",
 "SMALL_TIME",
 "synInput_tauRise",
 "synInput_tauDecay",
 "synInput_peakTime",
 "synInput_waveformFactor",
 "synInput_gbase",
 "synInput_erev",
 0,
 "synInput_g",
 "synInput_i",
 "iSyn",
 "i",
 0,
 "tsince",
 "tnextIdeal",
 "tnextUsed",
 "synInput_A",
 "synInput_B",
 0,
 "donotuse",
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
 	_p = nrn_prop_data_alloc(_mechtype, 33, _prop);
 	/*initialize range parameters*/
 	weight = 1;
 	averageRate = 0.1;
 	averageIsi = 10;
 	SMALL_TIME = 1e-09;
 	synInput_tauRise = 1;
 	synInput_tauDecay = 5;
 	synInput_peakTime = 2.0118;
 	synInput_waveformFactor = 1.86919;
 	synInput_gbase = 0.008;
 	synInput_erev = 20;
  }
 	_prop->param = _p;
 	_prop->param_size = 33;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 8, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 
#define _tqitem &(_ppvar[3]._pvoid)
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _poissonFiringSyn100Hz_reg() {
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
  hoc_register_prop_size(_mechtype, 33, 8);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "pointer");
  hoc_register_dparam_semantics(_mechtype, 3, "netsend");
  hoc_register_dparam_semantics(_mechtype, 4, "watch");
  hoc_register_dparam_semantics(_mechtype, 5, "watch");
  hoc_register_dparam_semantics(_mechtype, 6, "watch");
  hoc_register_dparam_semantics(_mechtype, 7, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 add_nrn_has_net_event(_mechtype);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 poissonFiringSyn100Hz /Users/padraig/NeuroMLlite/examples/test_files/x86_64/poissonFiringSyn100Hz.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "Mod file for component: Component(id=poissonFiringSyn100Hz type=poissonFiringSynapse)";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
static int noiseFromRandom(_threadargsproto_);
static int rates(_threadargsproto_);
static int seed(_threadargsprotocomma_ double);
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[5], _dlist1[5];
 static int states(_threadargsproto_);
 
static double _watch1_cond(_pnt) Point_process* _pnt; {
 	double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
	_thread= (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;
 	_p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
	v = NODEV(_pnt->node);
	return  ( t ) - ( tnextUsed ) ;
}
 
static double _watch2_cond(_pnt) Point_process* _pnt; {
 	double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
	_thread= (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;
 	_p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
	v = NODEV(_pnt->node);
	return  ( t ) - ( tnextUsed ) ;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   int _watch_rm = 0;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t;   if (_lflag == 1. ) {*(_tqitem) = 0;}
 {
   double _lweight ;
 if ( _lflag  == 1.0 ) {
       _nrn_watch_activate(_watch_array, _watch1_cond, 1, _pnt, _watch_rm++, 1000.0);
 }
   if ( _lflag  == 1000.0 ) {
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = tsince;
    double __primary = (0.0) - __state;
     __primary -= 0.5*dt*( - ( rate_tsince )  );
    tsince += __primary;
  } else {
 tsince = 0.0 ;
       }
 isi = - averageIsi * log ( 1.0 - random_float ( _threadargscomma_ 1.0 ) ) ;
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = tnextIdeal;
    double __primary = (( tnextIdeal + isi )) - __state;
     __primary -= 0.5*dt*( - ( rate_tnextIdeal )  );
    tnextIdeal += __primary;
  } else {
 tnextIdeal = ( tnextIdeal + isi ) ;
       }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = tnextUsed;
    double __primary = (tnextIdeal * H ( _threadargscomma_ ( tnextIdeal - t ) / t ) + ( t + SMALL_TIME ) * H ( _threadargscomma_ ( t - tnextIdeal ) / t )) - __state;
     __primary -= 0.5*dt*( - ( rate_tnextUsed )  );
    tnextUsed += __primary;
  } else {
 tnextUsed = tnextIdeal * H ( _threadargscomma_ ( tnextIdeal - t ) / t ) + ( t + SMALL_TIME ) * H ( _threadargscomma_ ( t - tnextIdeal ) / t ) ;
       }
 _lweight = 1.0 ;
       if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = synInput_A;
    double __primary = (synInput_A + ( _lweight * synInput_waveformFactor )) - __state;
     __primary -= 0.5*dt*( - ( rate_synInput_A )  );
    synInput_A += __primary;
  } else {
 synInput_A = synInput_A + ( _lweight * synInput_waveformFactor ) ;
       }
   if (nrn_netrec_state_adjust && !cvode_active_){
    /* discon state adjustment for cnexp case (rate uses no local variable) */
    double __state = synInput_B;
    double __primary = (synInput_B + ( _lweight * synInput_waveformFactor )) - __state;
     __primary -= 0.5*dt*( - ( rate_synInput_B )  );
    synInput_B += __primary;
  } else {
 synInput_B = synInput_B + ( _lweight * synInput_waveformFactor ) ;
       }
 net_event ( _pnt, t ) ;
       _nrn_watch_activate(_watch_array, _watch2_cond, 2, _pnt, _watch_rm++, 1000.0);
 }
   } }
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   rates ( _threadargs_ ) ;
   Dtsince = rate_tsince ;
   DtnextUsed = rate_tnextUsed ;
   DtnextIdeal = rate_tnextIdeal ;
   DsynInput_A = rate_synInput_A ;
   DsynInput_B = rate_synInput_B ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 rates ( _threadargs_ ) ;
 Dtsince = Dtsince  / (1. - dt*( 0.0 )) ;
 DtnextUsed = DtnextUsed  / (1. - dt*( 0.0 )) ;
 DtnextIdeal = DtnextIdeal  / (1. - dt*( 0.0 )) ;
 DsynInput_A = DsynInput_A  / (1. - dt*( 0.0 )) ;
 DsynInput_B = DsynInput_B  / (1. - dt*( 0.0 )) ;
  return 0;
}
 /*END CVODE*/
 static int states (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   rates ( _threadargs_ ) ;
    tsince = tsince - dt*(- ( rate_tsince ) ) ;
    tnextUsed = tnextUsed - dt*(- ( rate_tnextUsed ) ) ;
    tnextIdeal = tnextIdeal - dt*(- ( rate_tnextIdeal ) ) ;
    synInput_A = synInput_A - dt*(- ( rate_synInput_A ) ) ;
    synInput_B = synInput_B - dt*(- ( rate_synInput_B ) ) ;
   }
  return 0;
}
 
static int  rates ( _threadargsproto_ ) {
   synInput_g = synInput_gbase * ( synInput_B - synInput_A ) ;
   synInput_i = synInput_g * ( synInput_erev - v ) ;
   iSyn = synInput_i ;
   i = weight * iSyn ;
   rate_tsince = 1.0 ;
   rate_tnextUsed = 0.0 ;
   rate_tnextIdeal = 0.0 ;
   rate_synInput_A = - synInput_A / synInput_tauRise ;
   rate_synInput_B = - synInput_B / synInput_tauDecay ;
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
 
double random_float ( _threadargsprotocomma_ double _lmax ) {
   double _lrandom_float;
 _lrandom_float = exp ( - 1.0 * erand ( _threadargs_ ) ) * _lmax ;
   
return _lrandom_float;
 }
 
static double _hoc_random_float(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  random_float ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
static int  seed ( _threadargsprotocomma_ double _lx ) {
   set_seed ( _lx ) ;
    return 0; }
 
static double _hoc_seed(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r = 1.;
 seed ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
/*VERBATIM*/
double nrn_random_pick(void* r);
void* nrn_random_arg(int argpos);
 
double erand ( _threadargsproto_ ) {
   double _lerand;
 
/*VERBATIM*/
	if (_p_donotuse) {
		/*
		:Supports separate independent but reproducible streams for
		: each instance. However, the corresponding hoc Random
		: distribution MUST be set to Random.negexp(1)
		*/
		_lerand = nrn_random_pick(_p_donotuse);
	}else{
		/* only can be used in main thread */
		if (_nt != nrn_threads) {
           hoc_execerror("multithread random in NetStim"," only via hoc Random");
		}
 _lerand = exprand ( 1.0 ) ;
   
/*VERBATIM*/
	}
 
return _lerand;
 }
 
static double _hoc_erand(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  erand ( _p, _ppvar, _thread, _nt );
 return(_r);
}
 
static int  noiseFromRandom ( _threadargsproto_ ) {
   
/*VERBATIM*/
 {
	void** pv = (void**)(&_p_donotuse);
	if (ifarg(1)) {
		*pv = nrn_random_arg(1);
	}else{
		*pv = (void*)0;
	}
 }
  return 0; }
 
static double _hoc_noiseFromRandom(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r = 1.;
 noiseFromRandom ( _p, _ppvar, _thread, _nt );
 return(_r);
}
 
double H ( _threadargsprotocomma_ double _lx ) {
   double _lH;
 if ( _lx < 0.0 ) {
     _lH = 0.0 ;
     }
   else if ( _lx > 0.0 ) {
     _lH = 1.0 ;
     }
   else {
     _lH = 0.5 ;
     }
   
return _lH;
 }
 
static double _hoc_H(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  H ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 5;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 5; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  synInput_B = synInput_B0;
  synInput_A = synInput_A0;
  tnextUsed = tnextUsed0;
  tnextIdeal = tnextIdeal0;
  tsince = tsince0;
 {
   rates ( _threadargs_ ) ;
   rates ( _threadargs_ ) ;
   tsince = 0.0 ;
   isi = - averageIsi * log ( random_float ( _threadargscomma_ 1.0 ) ) ;
   tnextIdeal = isi ;
   tnextUsed = isi ;
   net_send ( _tqitem, (double*)0, _ppvar[1]._pvoid, t +  0.0 , 1.0 ) ;
   synInput_A = 0.0 ;
   synInput_B = 0.0 ;
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
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
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
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) += _rhs;
  }else
#endif
  {
	NODERHS(_nd) += _rhs;
  }
  if (_nt->_nrn_fast_imem) { _nt->_nrn_fast_imem->_nrn_sav_rhs[_ni[_iml]] += _rhs; }
#if EXTRACELLULAR
 if (_nd->_extnode) {
   *_nd->_extnode->_rhs[0] += _rhs;
 }
#endif
 
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
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) -= _g;
  }else
#endif
  {
	NODED(_nd) -= _g;
  }
  if (_nt->_nrn_fast_imem) { _nt->_nrn_fast_imem->_nrn_sav_d[_ni[_iml]] -= _g; }
#if EXTRACELLULAR
 if (_nd->_extnode) {
   *_nd->_extnode->_d[0] += _g;
 }
#endif
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if EXTRACELLULAR
 _nd = _ml->_nodelist[_iml];
 if (_nd->_extnode) {
    _v = NODEV(_nd) +_nd->_extnode->_v[0];
 }else
#endif
 {
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 }
 v=_v;
{
 {   states(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(tsince) - _p;  _dlist1[0] = &(Dtsince) - _p;
 _slist1[1] = &(tnextUsed) - _p;  _dlist1[1] = &(DtnextUsed) - _p;
 _slist1[2] = &(tnextIdeal) - _p;  _dlist1[2] = &(DtnextIdeal) - _p;
 _slist1[3] = &(synInput_A) - _p;  _dlist1[3] = &(DsynInput_A) - _p;
 _slist1[4] = &(synInput_B) - _p;  _dlist1[4] = &(DsynInput_B) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/Users/padraig/NeuroMLlite/examples/test_files/poissonFiringSyn100Hz.mod";
static const char* nmodl_file_text = 
  "TITLE Mod file for component: Component(id=poissonFiringSyn100Hz type=poissonFiringSynapse)\n"
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
  "    POINT_PROCESS poissonFiringSyn100Hz\n"
  "    ELECTRODE_CURRENT i\n"
  "    RANGE weight                            : property\n"
  "    RANGE averageRate                       : parameter\n"
  "    RANGE averageIsi                        : parameter\n"
  "    RANGE SMALL_TIME                        : parameter\n"
  "    \n"
  "    RANGE i                                 : exposure\n"
  "    RANGE synInput_tauRise                  : parameter\n"
  "    RANGE synInput_tauDecay                 : parameter\n"
  "    RANGE synInput_peakTime                 : parameter\n"
  "    RANGE synInput_waveformFactor           : parameter\n"
  "    RANGE synInput_gbase                    : parameter\n"
  "    RANGE synInput_erev                     : parameter\n"
  "    \n"
  "    RANGE synInput_g                        : exposure\n"
  "    \n"
  "    RANGE synInput_i                        : exposure\n"
  "    RANGE iSyn                              : derived variable\n"
  "    : Based on netstim.mod\n"
  "    THREADSAFE : only true if every instance has its own distinct Random\n"
  "    POINTER donotuse\n"
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
  "    weight = 1\n"
  "    averageRate = 0.1 (kHz)\n"
  "    averageIsi = 10 (ms)\n"
  "    SMALL_TIME = 1.0E-9 (ms)\n"
  "    synInput_tauRise = 1 (ms)\n"
  "    synInput_tauDecay = 5 (ms)\n"
  "    synInput_peakTime = 2.0117974 (ms)\n"
  "    synInput_waveformFactor = 1.8691859 \n"
  "    synInput_gbase = 0.008 (uS)\n"
  "    synInput_erev = 20 (mV)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "    v (mV)\n"
  "    isi (ms)                    : Not a state variable as far as Neuron's concerned...\n"
  "    \n"
  "    synInput_g (uS)                        : derived variable\n"
  "    \n"
  "    synInput_i (nA)                        : derived variable\n"
  "    \n"
  "    iSyn (nA)                              : derived variable\n"
  "    \n"
  "    i (nA)                                 : derived variable\n"
  "    rate_tsince (ms/ms)\n"
  "    rate_tnextUsed (ms/ms)\n"
  "    rate_tnextIdeal (ms/ms)\n"
  "    rate_synInput_A (/ms)\n"
  "    rate_synInput_B (/ms)\n"
  "    donotuse\n"
  "}\n"
  "\n"
  "STATE {\n"
  "    tsince (ms) \n"
  "    tnextIdeal (ms) \n"
  "    tnextUsed (ms) \n"
  "    synInput_A  \n"
  "    synInput_B  \n"
  "    \n"
  "}\n"
  "\n"
  "INITIAL {\n"
  "    rates()\n"
  "    rates() ? To ensure correct initialisation.\n"
  "    \n"
  "    tsince = 0\n"
  "    \n"
  "    isi = -  averageIsi  * log(random_float(1))\n"
  "    \n"
  "    tnextIdeal = isi\n"
  "    \n"
  "    tnextUsed = isi\n"
  "    \n"
  "    net_send(0, 1) : go to NET_RECEIVE block, flag 1, for initial state\n"
  "    \n"
  "    synInput_A = 0\n"
  "    \n"
  "    synInput_B = 0\n"
  "    \n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "    \n"
  "    SOLVE states METHOD cnexp\n"
  "    \n"
  "    \n"
  "}\n"
  "\n"
  "NET_RECEIVE(flag) {\n"
  "    \n"
  "    LOCAL weight\n"
  "    \n"
  "    \n"
  "    if (flag == 1) { : Setting watch for top level OnCondition...\n"
  "        WATCH (t >  tnextUsed) 1000\n"
  "    }\n"
  "    if (flag == 1000) {\n"
  "    \n"
  "        tsince = 0\n"
  "    \n"
  "        isi = -  averageIsi  * log(1 - random_float(1))\n"
  "    \n"
  "        tnextIdeal = (  tnextIdeal  +  isi  )\n"
  "    \n"
  "        tnextUsed = tnextIdeal  *H( (  tnextIdeal  -t)/t ) + (t+  SMALL_TIME  )*H( (t-  tnextIdeal  )/t )\n"
  "    \n"
  "        : Child: Component(id=synInput type=expTwoSynapse)\n"
  "    \n"
  "        : This child is a synapse; defining weight\n"
  "        weight = 1\n"
  "    \n"
  "        : paramMappings are: {poissonFiringSyn100Hz={tsince=tsince, tnextIdeal=tnextIdeal, tnextUsed=tnextUsed, isi=isi, weight=weight, averageRate=averageRate, averageIsi=averageIsi, SMALL_TIME=SMALL_TIME, i=i, iSyn=iSyn}, synInput={A=synInput_A, B=synInput_B, tauRise=synInput_tauRise, tauDecay=synInput_tauDecay, peakTime=synInput_peakTime, waveformFactor=synInput_w...\n"
  "        : state_discontinuity(synInput_A, synInput_A  + (weight *  synInput_waveformFactor ))\n"
  "        synInput_A = synInput_A  + (weight *  synInput_waveformFactor )\n"
  "    \n"
  "        : paramMappings are: {poissonFiringSyn100Hz={tsince=tsince, tnextIdeal=tnextIdeal, tnextUsed=tnextUsed, isi=isi, weight=weight, averageRate=averageRate, averageIsi=averageIsi, SMALL_TIME=SMALL_TIME, i=i, iSyn=iSyn}, synInput={A=synInput_A, B=synInput_B, tauRise=synInput_tauRise, tauDecay=synInput_tauDecay, peakTime=synInput_peakTime, waveformFactor=synInput_w...\n"
  "        : state_discontinuity(synInput_B, synInput_B  + (weight *  synInput_waveformFactor ))\n"
  "        synInput_B = synInput_B  + (weight *  synInput_waveformFactor )\n"
  "    \n"
  "        net_event(t)\n"
  "        WATCH (t >  tnextUsed) 1000\n"
  "    \n"
  "    }\n"
  "    \n"
  "}\n"
  "\n"
  "DERIVATIVE states {\n"
  "    rates()\n"
  "    tsince' = rate_tsince \n"
  "    tnextUsed' = rate_tnextUsed \n"
  "    tnextIdeal' = rate_tnextIdeal \n"
  "    synInput_A' = rate_synInput_A \n"
  "    synInput_B' = rate_synInput_B \n"
  "    \n"
  "}\n"
  "\n"
  "PROCEDURE rates() {\n"
  "    \n"
  "    synInput_g = synInput_gbase  * ( synInput_B  -  synInput_A ) ? evaluable\n"
  "    synInput_i = synInput_g  * ( synInput_erev  - v) ? evaluable\n"
  "    ? DerivedVariable is based on path: synapse/i, on: Component(id=poissonFiringSyn100Hz type=poissonFiringSynapse), from synapse; Component(id=synInput type=expTwoSynapse)\n"
  "    iSyn = synInput_i ? path based, prefix = \n"
  "    \n"
  "    i = weight  *  iSyn ? evaluable\n"
  "    rate_tsince = 1 ? Note units of all quantities used here need to be consistent!\n"
  "    rate_tnextUsed = 0 ? Note units of all quantities used here need to be consistent!\n"
  "    rate_tnextIdeal = 0 ? Note units of all quantities used here need to be consistent!\n"
  "    \n"
  "     \n"
  "    rate_synInput_A = - synInput_A  /  synInput_tauRise ? Note units of all quantities used here need to be consistent!\n"
  "    rate_synInput_B = - synInput_B  /  synInput_tauDecay ? Note units of all quantities used here need to be consistent!\n"
  "    \n"
  "     \n"
  "    \n"
  "}\n"
  "\n"
  "\n"
  ": Returns a float between 0 and max; implementation of random() as used in LEMS\n"
  "FUNCTION random_float(max) {\n"
  "    \n"
  "    : This is not ideal, getting an exponential dist random number and then turning back to uniform\n"
  "    : However this is the easiest what to ensure mod files with random methods fit into NEURON's\n"
  "    : internal framework for managing internal number generation.\n"
  "    random_float = exp(-1*erand())*max\n"
  "    \n"
  "}\n"
  "\n"
  ":****************************************************\n"
  ": Methods copied from netstim.mod in NEURON source\n"
  "\n"
  " \n"
  "PROCEDURE seed(x) {\n"
  "	set_seed(x)\n"
  "}\n"
  "\n"
  "VERBATIM\n"
  "double nrn_random_pick(void* r);\n"
  "void* nrn_random_arg(int argpos);\n"
  "ENDVERBATIM\n"
  "\n"
  "\n"
  "FUNCTION erand() {\n"
  "VERBATIM\n"
  "	if (_p_donotuse) {\n"
  "		/*\n"
  "		:Supports separate independent but reproducible streams for\n"
  "		: each instance. However, the corresponding hoc Random\n"
  "		: distribution MUST be set to Random.negexp(1)\n"
  "		*/\n"
  "		_lerand = nrn_random_pick(_p_donotuse);\n"
  "	}else{\n"
  "		/* only can be used in main thread */\n"
  "		if (_nt != nrn_threads) {\n"
  "           hoc_execerror(\"multithread random in NetStim\",\" only via hoc Random\");\n"
  "		}\n"
  "ENDVERBATIM\n"
  "		: the old standby. Cannot use if reproducible parallel sim\n"
  "		: independent of nhost or which host this instance is on\n"
  "		: is desired, since each instance on this cpu draws from\n"
  "		: the same stream\n"
  "		erand = exprand(1)\n"
  "VERBATIM\n"
  "	}\n"
  "ENDVERBATIM\n"
  "}\n"
  "\n"
  "PROCEDURE noiseFromRandom() {\n"
  "VERBATIM\n"
  " {\n"
  "	void** pv = (void**)(&_p_donotuse);\n"
  "	if (ifarg(1)) {\n"
  "		*pv = nrn_random_arg(1);\n"
  "	}else{\n"
  "		*pv = (void*)0;\n"
  "	}\n"
  " }\n"
  "ENDVERBATIM\n"
  "}\n"
  "\n"
  ": End of methods copied from netstim.mod in NEURON source\n"
  ":****************************************************\n"
  "\n"
  "\n"
  ": The Heaviside step function\n"
  "FUNCTION H(x) {\n"
  "    \n"
  "    if (x < 0) { H = 0 }\n"
  "    else if (x > 0) { H = 1 }\n"
  "    else { H = 0.5 }\n"
  "    \n"
  "}\n"
  "\n"
  ;
#endif
