#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _ampa_reg(void);
extern void _iclamp0_reg(void);
extern void _kChan_reg(void);
extern void _naChan_reg(void);
extern void _passiveChan_reg(void);
extern void _poissonFiringSyn_reg(void);
extern void _poissonFiringSyn100Hz_reg(void);
extern void _synInput_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," ampa.mod");
    fprintf(stderr," iclamp0.mod");
    fprintf(stderr," kChan.mod");
    fprintf(stderr," naChan.mod");
    fprintf(stderr," passiveChan.mod");
    fprintf(stderr," poissonFiringSyn.mod");
    fprintf(stderr," poissonFiringSyn100Hz.mod");
    fprintf(stderr," synInput.mod");
    fprintf(stderr, "\n");
  }
  _ampa_reg();
  _iclamp0_reg();
  _kChan_reg();
  _naChan_reg();
  _passiveChan_reg();
  _poissonFiringSyn_reg();
  _poissonFiringSyn100Hz_reg();
  _synInput_reg();
}
