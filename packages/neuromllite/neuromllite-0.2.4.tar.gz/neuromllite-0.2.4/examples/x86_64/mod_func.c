#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _ampa_reg(void);
extern void _ampaSyn_reg(void);
extern void _gaba_reg(void);
extern void _gabaSyn_reg(void);
extern void _i_clamp_reg(void);
extern void _ifcell_reg(void);
extern void _kChan_reg(void);
extern void _naChan_reg(void);
extern void _passiveChan_reg(void);
extern void _poissonFiringSyn_reg(void);
extern void _poisson_input_reg(void);
extern void _testcell_reg(void);
extern void _testcell2_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," ampa.mod");
    fprintf(stderr," ampaSyn.mod");
    fprintf(stderr," gaba.mod");
    fprintf(stderr," gabaSyn.mod");
    fprintf(stderr," i_clamp.mod");
    fprintf(stderr," ifcell.mod");
    fprintf(stderr," kChan.mod");
    fprintf(stderr," naChan.mod");
    fprintf(stderr," passiveChan.mod");
    fprintf(stderr," poissonFiringSyn.mod");
    fprintf(stderr," poisson_input.mod");
    fprintf(stderr," testcell.mod");
    fprintf(stderr," testcell2.mod");
    fprintf(stderr, "\n");
  }
  _ampa_reg();
  _ampaSyn_reg();
  _gaba_reg();
  _gabaSyn_reg();
  _i_clamp_reg();
  _ifcell_reg();
  _kChan_reg();
  _naChan_reg();
  _passiveChan_reg();
  _poissonFiringSyn_reg();
  _poisson_input_reg();
  _testcell_reg();
  _testcell2_reg();
}
