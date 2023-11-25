#define SINGLE_FILE
/**
  ******************************************************************************
  * @file    number.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    2 february 2021
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef __NUMBER_H__
#define __NUMBER_H__

#include <stdint.h>
#include <stddef.h>
#include <math.h>

#define True 1
#define False 0

#define _clamp_to(type, number) clamp_to_number_t_ ## type (number)
#define clamp_to(type, number) _clamp_to(type, number)
#define _scale(type, number, scale_factor) scale_number_t_ ## type (number, scale_factor)
#define scale(type, number, scale_factor) _scale(type, number, scale_factor)

// Idea 1: Write the smallest min max interval of the net, could be an issue for hybrid int type network
// Idea 2: listing any interval and add type in name in a switch case like <- better but painfull
// #define NUMBER_MIN		// Max value for this numeric type
// #define NUMBER_MAX		// Min value for this numeric type

// // Idea 1: List of all types and write any corresponding function 
// typedef  number_t;		// Standard size numeric type used for weights and activations
// typedef  long_number_t;	// Long numeric type used for intermediate results

#define NUMBER_MIN_INT32_T -2147483648
#define NUMBER_MAX_INT32_T 2147483647

static inline int64_t min_int32_t(
    int64_t a,
    int64_t b) {
	if (a <= b)
		return a;
	return b;
}

static inline int64_t max_int32_t(
    int64_t a,
    int64_t b) {
	if (a >= b)
		return a;
	return b;
}

static inline int64_t scale_number_t_int32_t(
  int64_t number, int scale_factor) {
  if (scale_factor < 0)
    return number << - scale_factor;
  else 
    return number >> scale_factor;
}
static inline int32_t clamp_to_number_t_int32_t(
  int64_t number) {
	return (int32_t) max_int32_t(
      NUMBER_MIN_INT32_T,
      min_int32_t(
        NUMBER_MAX_INT32_T, number));
}

#define NUMBER_MIN_FLOAT -2147483648
#define NUMBER_MAX_FLOAT 2147483647

static inline float min_float(
    float a,
    float b) {
	if (a <= b)
		return a;
	return b;
}

static inline float max_float(
    float a,
    float b) {
	if (a >= b)
		return a;
	return b;
}

static inline float scale_number_t_float(
  float number, int scale_factor) {
	return number;
}
static inline float clamp_to_number_t_float(
  float number) {
	return (float) number;
}





static inline void int64_t_to_float(int64_t * tabint, float * tabfloat, long tabdim, int scale_factor){
  for (int i=0; i<tabdim; i++){
    tabfloat[i] = (float)tabint[i] / (1<<scale_factor);
  }
}

static inline void int32_t_to_float(int32_t * tabint, float * tabfloat, long tabdim, int scale_factor){
  for (int i=0; i<tabdim; i++){
    tabfloat[i] = (float)tabint[i] / (1<<scale_factor);
  }
}

static inline void int16_t_to_float(int16_t * tabint, float * tabfloat, long tabdim, int scale_factor){
  for (int i=0; i<tabdim; i++){
    tabfloat[i] = ((float)tabint[i]) / (1<<scale_factor);
  }
}

static inline void int8_t_to_float(int8_t * tabint, float * tabfloat, long tabdim, int scale_factor){
  for (int i=0; i<tabdim; i++){
    tabfloat[i] = ((float)tabint[i]) / (1<<scale_factor);
  }
}
#endif //__NUMBER_H__

#ifdef __cplusplus
} // extern "C"
#endif
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV1D_H_
#define _CONV1D_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      9
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv1d_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv1d(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV1D_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv1d.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      9
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_RELU

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv1d(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_RELU
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    9
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  3


const float  conv1d_bias[CONV_FILTERS] = {0x1.ae179a0000000p-2, -0x1.57bbd00000000p-4, -0x1.f349240000000p-5, 0x1.96196c0000000p-3, 0x1.96daac0000000p-4, -0x1.4fc74a0000000p-2, 0x1.81696a0000000p-2, 0x1.93fb060000000p-2}
;

const float  conv1d_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{0x1.4999800000000p-2, 0x1.8558000000000p-8, 0x1.fac2ec0000000p-5, -0x1.db1de60000000p-3, 0x1.fdde480000000p-4, 0x1.9cadee0000000p-5, -0x1.0fdc020000000p-1, -0x1.bbd4580000000p-4, -0x1.3f0d540000000p-4}
, {0x1.0aacce0000000p-2, 0x1.7f4b520000000p-4, -0x1.5e63200000000p-5, 0x1.407a2e0000000p-3, 0x1.ddfd840000000p-4, 0x1.b17ca80000000p-4, -0x1.7040c40000000p-3, -0x1.5e50b60000000p-3, -0x1.7832440000000p-5}
, {0x1.c7bad40000000p-2, 0x1.efb5480000000p-6, 0x1.28f0ea0000000p-3, 0x1.d78a960000000p-3, -0x1.eaa25a0000000p-4, -0x1.5941e20000000p-3, -0x1.4efb940000000p-1, 0x1.cdb5480000000p-3, 0x1.59850e0000000p-4}
}
, {{-0x1.8dcd500000000p-3, -0x1.380a220000000p-2, 0x1.a7db800000000p-3, 0x1.7e25120000000p-2, 0x1.2ea5040000000p-3, 0x1.315ef60000000p-2, 0x1.4099860000000p-2, 0x1.941ec80000000p-3, 0x1.926c040000000p-3}
, {-0x1.88f7720000000p-2, -0x1.6194de0000000p-2, -0x1.ecf0c00000000p-3, -0x1.6b3b220000000p-6, 0x1.ee76600000000p-3, 0x1.4dcdf20000000p-5, 0x1.6e13260000000p-3, 0x1.bc367e0000000p-3, 0x1.114cb80000000p-3}
, {-0x1.12d64a0000000p-1, 0x1.19ff320000000p-5, -0x1.bd05ca0000000p-2, -0x1.aefa240000000p-3, 0x1.702f440000000p-3, 0x1.d772ec0000000p-5, 0x1.b4c1de0000000p-6, 0x1.26ba800000000p-1, 0x1.941dae0000000p-3}
}
, {{-0x1.2e783a0000000p-2, -0x1.8fca660000000p-3, -0x1.d06b3e0000000p-4, 0x1.715ab00000000p-3, 0x1.f28d3a0000000p-4, 0x1.0ac44e0000000p-3, 0x1.95cef80000000p-9, -0x1.5f0e8e0000000p-1, -0x1.2e4b960000000p-5}
, {-0x1.a69dcc0000000p-8, 0x1.fa5a1c0000000p-5, -0x1.266ffc0000000p-2, -0x1.592a200000000p-5, -0x1.9c6c8c0000000p-5, -0x1.4247ce0000000p-3, 0x1.7228540000000p-2, -0x1.06b2040000000p-1, -0x1.7d1a0e0000000p-4}
, {0x1.6f5d440000000p-3, 0x1.4bb9680000000p-2, -0x1.fa273a0000000p-8, -0x1.0633300000000p-2, -0x1.8b2ef60000000p-4, 0x1.2349cc0000000p-3, 0x1.7c69a00000000p-2, -0x1.bbe2740000000p-2, 0x1.4f14d00000000p-2}
}
, {{-0x1.3ea5360000000p-3, 0x1.9930ee0000000p-5, -0x1.bff6220000000p-4, 0x1.4ad9fa0000000p-4, -0x1.3934660000000p-6, -0x1.2b86440000000p-3, -0x1.b656e20000000p-4, -0x1.20fa700000000p-2, -0x1.84e8f80000000p-5}
, {-0x1.d1e15c0000000p-2, 0x1.6c5cc80000000p-3, -0x1.5d40900000000p-2, -0x1.30c2360000000p-3, 0x1.5416200000000p-4, -0x1.6491140000000p-6, -0x1.01070a0000000p-3, 0x1.6ec6480000000p-6, -0x1.29fcc60000000p-5}
, {-0x1.32e50c0000000p-2, 0x1.5e22c80000000p-2, -0x1.ccff2a0000000p-2, 0x1.e9ddda0000000p-6, -0x1.bc7c960000000p-5, -0x1.c174840000000p-4, -0x1.903aec0000000p-3, 0x1.ec58bc0000000p-5, -0x1.14021e0000000p-5}
}
, {{0x1.d62b3a0000000p-3, -0x1.331ce60000000p-2, -0x1.0b81040000000p-2, 0x1.b9d1dc0000000p-3, 0x1.0db34c0000000p-2, 0x1.66a7d20000000p-3, 0x1.63276c0000000p-4, -0x1.a03d680000000p-5, 0x1.78794c0000000p-8}
, {0x1.9ea9e80000000p-2, -0x1.0de9300000000p-2, -0x1.651ade0000000p-3, -0x1.2894020000000p-4, -0x1.1c48680000000p-4, 0x1.0aa5a00000000p-4, 0x1.2745ec0000000p-2, -0x1.2e3ca00000000p-7, -0x1.0f6f920000000p-4}
, {0x1.0f5f900000000p-1, -0x1.3755d00000000p-4, -0x1.1693da0000000p-6, -0x1.83e5740000000p-6, -0x1.d155d60000000p-2, -0x1.61acdc0000000p-2, -0x1.bf87480000000p-6, 0x1.0912860000000p-2, 0x1.c3fdac0000000p-3}
}
, {{0x1.619d9c0000000p-3, 0x1.65e6be0000000p-3, 0x1.0f8e880000000p-10, 0x1.2f8cbe0000000p-3, 0x1.b0ce820000000p-4, -0x1.b817140000000p-8, 0x1.6bf8160000000p-3, -0x1.332f1e0000000p-1, 0x1.7e2f800000000p-5}
, {0x1.55b3b20000000p-6, 0x1.93b9d20000000p-5, 0x1.cddeb20000000p-3, 0x1.305f220000000p-4, -0x1.bf02700000000p-7, 0x1.15b26c0000000p-4, 0x1.479fdc0000000p-4, -0x1.c3ff040000000p-2, -0x1.06f4520000000p-3}
, {-0x1.4b81a20000000p-2, -0x1.e6d9840000000p-5, 0x1.1fd6b40000000p-3, -0x1.65385a0000000p-2, -0x1.b59b4a0000000p-3, -0x1.7a9a220000000p-4, -0x1.3ee01a0000000p-4, -0x1.17203c0000000p-2, 0x1.e5abfa0000000p-4}
}
, {{-0x1.f0ee4e0000000p-7, -0x1.45d49e0000000p-3, -0x1.bff9fa0000000p-5, 0x1.8716c00000000p-2, 0x1.c1f7360000000p-4, -0x1.b1b5540000000p-5, 0x1.bc4f120000000p-5, -0x1.1510e00000000p-3, -0x1.4e038c0000000p-5}
, {-0x1.b0e03c0000000p-2, -0x1.999aa00000000p-2, -0x1.b9ae380000000p-3, 0x1.4b6c360000000p-3, 0x1.7bb5b40000000p-3, 0x1.565c620000000p-5, -0x1.241ba00000000p-5, -0x1.6ae5700000000p-2, 0x1.34dd7a0000000p-4}
, {-0x1.5d39ee0000000p-2, -0x1.175df80000000p-2, -0x1.8e696c0000000p-2, -0x1.3030bc0000000p-3, 0x1.313dc20000000p-6, 0x1.3d30200000000p-3, 0x1.07b93e0000000p-5, -0x1.a358240000000p-3, 0x1.212d4e0000000p-3}
}
, {{-0x1.8638960000000p-4, -0x1.02480e0000000p-3, -0x1.d186d20000000p-2, 0x1.6291a60000000p-3, -0x1.b6d8960000000p-3, -0x1.bbbb8c0000000p-3, -0x1.6ca54a0000000p-3, -0x1.842be40000000p-3, -0x1.0880d60000000p-6}
, {-0x1.6c27ba0000000p-4, 0x1.4e552c0000000p-3, -0x1.5726240000000p-3, 0x1.9e07380000000p-3, -0x1.c3e4d00000000p-7, -0x1.18ebe00000000p-5, -0x1.2506e00000000p-7, -0x1.2b26340000000p-4, -0x1.25ce880000000p-4}
, {-0x1.8f230e0000000p-2, 0x1.a7a1b80000000p-3, -0x1.0ad7da0000000p-2, -0x1.e62cac0000000p-4, -0x1.9e8b200000000p-3, -0x1.b4a0340000000p-3, -0x1.5f6acc0000000p-7, 0x1.2d2ea00000000p-5, 0x1.0e65700000000p-3}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV1D_1_H_
#define _CONV1D_1_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv1d_1_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv1d_1(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV1D_1_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv1d_1.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv1d_1(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_LINEAR
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    8
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  3


const float  conv1d_1_bias[CONV_FILTERS] = {0x1.02a0780000000p-2, 0x1.758eea0000000p-5, -0x1.fcc8020000000p-3, 0x1.f471780000000p-5, 0x1.edb1240000000p-3, -0x1.7680260000000p-3, 0x1.901b220000000p-3, -0x1.b22cc00000000p-4}
;

const float  conv1d_1_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{-0x1.0c9df00000000p-2, 0x1.70583e0000000p-1, 0x1.e0d7620000000p-6, -0x1.7076b40000000p-5, -0x1.fb20520000000p-6, -0x1.9a04e80000000p-3, -0x1.42786e0000000p-5, -0x1.79e93e0000000p-7}
, {-0x1.5c00d00000000p-6, 0x1.1dac320000000p-1, 0x1.41f82e0000000p-4, 0x1.c937ce0000000p-4, -0x1.16d1880000000p-4, -0x1.8904940000000p-4, -0x1.fe71c00000000p-4, 0x1.81e53a0000000p-4}
, {-0x1.e66d6a0000000p-3, -0x1.7e09420000000p-4, 0x1.d64c4a0000000p-4, 0x1.2245ae0000000p-2, -0x1.f1e5000000000p-3, 0x1.d85d420000000p-6, -0x1.69ad2a0000000p-5, 0x1.02991c0000000p-3}
}
, {{-0x1.ac8ad60000000p-2, -0x1.f5e6800000000p-4, -0x1.6e539a0000000p-3, 0x1.122a900000000p-4, -0x1.e5b02c0000000p-4, 0x1.8e799a0000000p-3, -0x1.78ed0c0000000p-4, 0x1.7786200000000p-4}
, {-0x1.0da6fe0000000p-2, -0x1.0354ac0000000p-4, 0x1.460dfc0000000p-3, 0x1.c323a60000000p-3, -0x1.a38db80000000p-3, -0x1.bba55c0000000p-3, -0x1.24f9980000000p-4, 0x1.1da3720000000p-3}
, {-0x1.ab0fc60000000p-2, -0x1.86d0260000000p-2, 0x1.c960900000000p-4, 0x1.d81f8c0000000p-3, -0x1.3075920000000p-3, 0x1.49b3f00000000p-5, 0x1.76cca00000000p-4, 0x1.e1ba940000000p-3}
}
, {{-0x1.2b72ee0000000p-3, -0x1.47d39c0000000p-4, -0x1.dcb7d20000000p-4, -0x1.6266740000000p-5, 0x1.bfcb2c0000000p-6, -0x1.ecc2400000000p-4, -0x1.1131600000000p-3, -0x1.60cb5a0000000p-3}
, {-0x1.9ea3be0000000p-5, 0x1.e02d1a0000000p-5, 0x1.07e14e0000000p-5, -0x1.0483880000000p-3, -0x1.b1ea780000000p-3, 0x1.39744c0000000p-4, -0x1.281fd20000000p-5, 0x1.edfc920000000p-4}
, {-0x1.7125c60000000p-3, -0x1.32b9c40000000p-4, -0x1.01243a0000000p-7, -0x1.a96e300000000p-3, 0x1.aae84a0000000p-9, -0x1.846e680000000p-3, -0x1.a562080000000p-5, -0x1.068f2e0000000p-2}
}
, {{0x1.fc9a520000000p-2, 0x1.baf8000000000p-4, 0x1.11976c0000000p-2, 0x1.1b387a0000000p-2, 0x1.f03bea0000000p-8, -0x1.09f56e0000000p-5, -0x1.724f5e0000000p-4, -0x1.69f99a0000000p-3}
, {0x1.d51e060000000p-2, -0x1.24fc200000000p-3, -0x1.1bc2000000000p-7, 0x1.a5940e0000000p-3, 0x1.d0bb880000000p-4, -0x1.4bd4540000000p-3, -0x1.dc20820000000p-7, 0x1.01b17c0000000p-3}
, {0x1.41b6900000000p-2, -0x1.abd5220000000p-3, -0x1.5b0d340000000p-14, -0x1.22ea920000000p-2, 0x1.0091360000000p-3, 0x1.0bdaa80000000p-3, -0x1.01da220000000p-1, 0x1.46ca740000000p-2}
}
, {{-0x1.bcdc160000000p-5, 0x1.8195400000000p-4, -0x1.bd04ca0000000p-3, 0x1.254bba0000000p-5, 0x1.8454060000000p-3, 0x1.97e7600000000p-5, 0x1.9e9c200000000p-6, -0x1.73c5c00000000p-2}
, {-0x1.8c5c180000000p-2, -0x1.15d3ae0000000p-4, 0x1.1878cc0000000p-5, -0x1.808a5a0000000p-2, 0x1.1fa45c0000000p-2, 0x1.f4a9340000000p-3, -0x1.618e020000000p-4, -0x1.b3a5380000000p-3}
, {-0x1.2a4fb40000000p-2, -0x1.e1b2f20000000p-3, 0x1.1db5b40000000p-2, -0x1.4a55a20000000p-2, -0x1.71da4e0000000p-7, -0x1.0e87ae0000000p-5, 0x1.5908ee0000000p-4, -0x1.68e4c40000000p-4}
}
, {{0x1.9799ba0000000p-2, -0x1.7b2f7a0000000p-3, -0x1.5085da0000000p-2, -0x1.6b897a0000000p-3, 0x1.2d72740000000p-2, 0x1.69677c0000000p-5, -0x1.cbd8140000000p-3, 0x1.edb3520000000p-8}
, {0x1.0141520000000p-4, -0x1.27c5820000000p-2, -0x1.c0d5d80000000p-4, -0x1.0f19ae0000000p-4, -0x1.506c560000000p-6, 0x1.254e400000000p-2, -0x1.2d855a0000000p-2, -0x1.163de00000000p-4}
, {-0x1.d8e6fa0000000p-6, -0x1.1f77ea0000000p-3, -0x1.68ea880000000p-5, -0x1.d44cc20000000p-3, 0x1.7f82e60000000p-3, -0x1.cb71420000000p-4, -0x1.3cb3dc0000000p-2, -0x1.a9f95e0000000p-3}
}
, {{-0x1.7d178c0000000p-3, 0x1.e1b5600000000p-8, -0x1.a9df580000000p-6, -0x1.53b5d80000000p-6, 0x1.c9fc360000000p-4, 0x1.badfc40000000p-4, 0x1.2002140000000p-2, 0x1.a9f2d00000000p-3}
, {0x1.22e1900000000p-4, 0x1.e325780000000p-3, 0x1.40788e0000000p-3, 0x1.84e9c20000000p-5, -0x1.e34f5e0000000p-3, -0x1.dd608c0000000p-6, 0x1.59bd6c0000000p-4, 0x1.458ba80000000p-3}
, {0x1.34d22c0000000p-4, 0x1.dda0ae0000000p-4, -0x1.251bc60000000p-4, 0x1.bc56f60000000p-3, -0x1.3f9daa0000000p-2, 0x1.ec850c0000000p-8, 0x1.1975d20000000p-5, 0x1.3d24780000000p-2}
}
, {{-0x1.168f6a0000000p-1, -0x1.50297c0000000p-1, 0x1.41086c0000000p-2, 0x1.51d3580000000p-4, 0x1.a679280000000p-4, 0x1.c98dda0000000p-6, 0x1.9e35420000000p-6, -0x1.4646180000000p-14}
, {-0x1.d1843e0000000p-2, -0x1.1630380000000p-1, 0x1.f764680000000p-3, 0x1.20126c0000000p-5, 0x1.2054ee0000000p-2, 0x1.828a2a0000000p-2, -0x1.02e5b80000000p-2, -0x1.94d2ee0000000p-10}
, {-0x1.cd2f080000000p-3, -0x1.54eb920000000p-2, 0x1.1cfb620000000p-5, 0x1.1128780000000p-2, -0x1.bef5880000000p-6, 0x1.c591ae0000000p-3, -0x1.a191be0000000p-3, -0x1.1ae40a0000000p-5}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    maxpool1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _MAX_POOLING1D_H_
#define _MAX_POOLING1D_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   128
#define POOL_SIZE       2
#define POOL_STRIDE     2
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

typedef float max_pooling1d_output_type[POOL_LENGTH][INPUT_CHANNELS];

#if 0
void max_pooling1d(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  number_t output[POOL_LENGTH][INPUT_CHANNELS]); 	// OUT
#endif

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH

#endif//_MAX_POOLING1D_H_
/**
  ******************************************************************************
  * @file    maxpool.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "max_pooling1d.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   128
#define POOL_SIZE       2
#define POOL_STRIDE     2
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

#define ACTIVATION_RELU

// For fixed point quantization
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void max_pooling1d(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  NUMBER_T output[POOL_LENGTH][INPUT_CHANNELS]) {	// OUT

  unsigned short pos_x, k; 	// loop indexes for output volume
  unsigned int x;
  static LONG_NUMBER_T max[INPUT_CHANNELS];

  for (pos_x = 0; pos_x < POOL_LENGTH; pos_x++) {
    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef ACTIVATION_LINEAR
      max[k] = input[pos_x*POOL_STRIDE][k];
      x = 1;
#elif defined(ACTIVATION_RELU)
      max[k] = 0;
      x = 0;
#endif
    }

    for (; x < POOL_SIZE; x++) {
      for (k = 0; k < INPUT_CHANNELS; k++) {
        if (max[k] < input[(pos_x * POOL_STRIDE) + x][k])
          max[k] = input[(pos_x * POOL_STRIDE) + x][k];
      }
    }

    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef WITH_CMSIS_NN
// Not really CMSIS-NN since using arm_relu_q* is not more efficient, but use SSAT anyway
#if ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR > 0
      output[pos_x][k] = __SSAT(max[k] >> (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#else
      output[pos_x][k] = __SSAT(max[k] << (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#endif
#else
      max[k] = scale(NUMBER_T, max[k], INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, max[k]);
#endif
    }
  }
}

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH
#undef ACTIVATION_RELU
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV_SHORTCUT_H_
#define _CONV_SHORTCUT_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    1
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    0
#define ZEROPADDING_RIGHT   0

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv_shortcut_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv_shortcut(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV_SHORTCUT_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv_shortcut.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       128
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    1
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    0
#define ZEROPADDING_RIGHT   0

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv_shortcut(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_LINEAR
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    8
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  1


const float  conv_shortcut_bias[CONV_FILTERS] = {0x1.174efe0000000p-4, -0x1.4c3f760000000p-2, 0x1.637a300000000p-2, -0x1.abfece0000000p-3, 0x1.d54f560000000p-3, 0x1.cf6e380000000p-2, -0x1.926dea0000000p-3, -0x1.096afc0000000p-2}
;

const float  conv_shortcut_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{-0x1.f973300000000p-4, -0x1.0e2cca0000000p-1, 0x1.5364120000000p-4, 0x1.6933700000000p-2, 0x1.4f0c920000000p-3, 0x1.985aa20000000p-2, 0x1.012f0c0000000p-2, 0x1.1a2e400000000p-2}
}
, {{-0x1.a22b580000000p-2, 0x1.8aa9e40000000p-3, 0x1.4a72ec0000000p-2, -0x1.712b480000000p-2, 0x1.3482160000000p-2, -0x1.b8df6e0000000p-3, 0x1.8c44c00000000p-3, -0x1.a4d4640000000p-5}
}
, {{0x1.6e4e960000000p-6, 0x1.b73e200000000p-5, -0x1.8d35e00000000p-5, -0x1.8eb5b40000000p-3, -0x1.46b98e0000000p-2, -0x1.002f440000000p-4, 0x1.9e2b7a0000000p-4, 0x1.bc43ca0000000p-4}
}
, {{0x1.46f4a60000000p-3, -0x1.1788f40000000p-1, 0x1.b02aaa0000000p-4, 0x1.566c460000000p-3, 0x1.1d570c0000000p-1, 0x1.0e9bbc0000000p-4, -0x1.f404da0000000p-2, 0x1.b079e60000000p-3}
}
, {{-0x1.bcf7cc0000000p-6, 0x1.e23b400000000p-6, -0x1.560e6e0000000p-2, -0x1.6f64040000000p-3, 0x1.8bb53e0000000p-2, 0x1.92260c0000000p-3, -0x1.ec58620000000p-2, -0x1.8eaa200000000p-4}
}
, {{-0x1.4e6b4c0000000p-1, -0x1.095b7a0000000p-5, -0x1.15f7580000000p-1, -0x1.62c92e0000000p-5, 0x1.3e0f8a0000000p-3, -0x1.793f4c0000000p-1, -0x1.6c6b0e0000000p-2, -0x1.776d200000000p-5}
}
, {{0x1.ef68e00000000p-4, 0x1.2ec4480000000p-3, 0x1.39c82c0000000p-3, 0x1.a3e9320000000p-4, -0x1.4ee1840000000p-2, 0x1.5aec1c0000000p-5, 0x1.46b8300000000p-4, -0x1.6e748e0000000p-2}
}
, {{0x1.88ce6e0000000p-3, 0x1.dbb9300000000p-2, -0x1.61303c0000000p-3, -0x1.ecc9e00000000p-2, 0x1.f50aa00000000p-3, 0x1.1ef25e0000000p-2, 0x1.e5619a0000000p-2, -0x1.264ef60000000p-1}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV_REF_H_
#define _CONV_REF_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv_ref_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv_ref(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV_REF_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv_ref.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv_ref(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_LINEAR
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    8
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  3


const float  conv_ref_bias[CONV_FILTERS] = {0x1.1b3f640000000p-5, -0x1.9097140000000p-4, 0x1.14df780000000p-5, 0x1.394c440000000p-4, -0x1.b4897a0000000p-5, 0x1.2721580000000p-2, -0x1.486b9e0000000p-5, 0x1.594d060000000p-5}
;

const float  conv_ref_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{-0x1.670f180000000p-4, 0x1.0ce3080000000p-3, -0x1.fabdbc0000000p-4, 0x1.a863180000000p-10, 0x1.93d8560000000p-3, -0x1.64bb3e0000000p-2, 0x1.887f940000000p-3, 0x1.0fb26c0000000p-2}
, {-0x1.3ed5f20000000p-4, 0x1.db7f760000000p-7, 0x1.e1db380000000p-3, -0x1.0b4af60000000p-3, -0x1.0827d60000000p-2, -0x1.3961040000000p-2, 0x1.5d8bf60000000p-3, 0x1.b234e60000000p-4}
, {0x1.257f5c0000000p-2, 0x1.5f34d60000000p-2, 0x1.9a9e680000000p-3, 0x1.95a7d80000000p-2, -0x1.4931d40000000p-2, -0x1.9333960000000p-5, -0x1.e70f480000000p-5, 0x1.fa45a40000000p-3}
}
, {{0x1.7bf48a0000000p-4, 0x1.d9d46e0000000p-3, 0x1.30f41a0000000p-6, -0x1.245ddc0000000p-6, 0x1.8f14800000000p-3, -0x1.ce7bcc0000000p-4, 0x1.37c39e0000000p-3, 0x1.7264220000000p-4}
, {0x1.be69360000000p-5, 0x1.79df540000000p-4, 0x1.0711260000000p-6, -0x1.3c54c80000000p-6, 0x1.6da2520000000p-2, 0x1.ca48720000000p-2, -0x1.f877440000000p-6, -0x1.675a580000000p-5}
, {-0x1.b93efa0000000p-4, -0x1.09a7f00000000p-2, -0x1.965b2e0000000p-6, 0x1.87a6b60000000p-2, -0x1.d8179c0000000p-4, 0x1.d0c5b20000000p-3, -0x1.41e6980000000p-2, 0x1.1b292a0000000p-2}
}
, {{0x1.f3849a0000000p-4, -0x1.1e9fa80000000p-4, 0x1.47a50c0000000p-3, 0x1.cfbb160000000p-2, -0x1.4d2bc80000000p-2, 0x1.2110f60000000p-4, 0x1.301c9a0000000p-3, -0x1.e5c13e0000000p-2}
, {-0x1.540dcc0000000p-2, -0x1.652e800000000p-2, 0x1.7cd0f00000000p-5, 0x1.86c0360000000p-2, -0x1.5450440000000p-4, 0x1.463bc20000000p-3, 0x1.cddd620000000p-7, -0x1.c6b0240000000p-1}
, {-0x1.cb4dca0000000p-4, -0x1.3b7dc20000000p-2, -0x1.12aed80000000p-4, 0x1.6bb8540000000p-2, -0x1.71baee0000000p-4, 0x1.51dc6a0000000p-4, -0x1.19dab80000000p-2, -0x1.3912a60000000p-1}
}
, {{-0x1.5b6d5e0000000p-3, -0x1.693e060000000p-3, 0x1.534a680000000p-3, 0x1.44df4e0000000p-2, 0x1.41e4920000000p-6, 0x1.5647cc0000000p-3, -0x1.457ac60000000p-2, 0x1.238fbc0000000p-2}
, {-0x1.260dda0000000p-2, 0x1.ac8dac0000000p-4, -0x1.34f2680000000p-3, 0x1.2cba460000000p-4, 0x1.1a016c0000000p-2, 0x1.5653a20000000p-2, -0x1.1c89960000000p-2, 0x1.3cd3ba0000000p-3}
, {-0x1.58db900000000p-2, 0x1.47486c0000000p-3, -0x1.7635bc0000000p-5, 0x1.635da80000000p-6, 0x1.9ca9f20000000p-2, 0x1.c714140000000p-4, 0x1.1038b60000000p-3, 0x1.a151780000000p-5}
}
, {{0x1.0f23e60000000p-6, -0x1.c384360000000p-4, -0x1.f58f360000000p-3, -0x1.ee910c0000000p-5, 0x1.fca7e20000000p-4, -0x1.db93e20000000p-9, 0x1.b077e80000000p-4, 0x1.e3ae040000000p-3}
, {0x1.4117be0000000p-2, -0x1.12484a0000000p-3, -0x1.28270a0000000p-3, -0x1.771aea0000000p-6, 0x1.cc5fe00000000p-4, -0x1.8108960000000p-6, -0x1.1d77040000000p-3, -0x1.3aef960000000p-2}
, {-0x1.e7185c0000000p-2, -0x1.efb22c0000000p-4, 0x1.ff3bc20000000p-4, 0x1.20de3c0000000p-3, 0x1.137d660000000p-3, 0x1.31ae5c0000000p-2, -0x1.8349a00000000p-3, -0x1.ab2ee80000000p-3}
}
, {{0x1.fe76f20000000p-3, 0x1.b564d00000000p-4, -0x1.1fde200000000p-3, 0x1.dfa7780000000p-3, 0x1.8502260000000p-4, 0x1.0a25aa0000000p-2, 0x1.9c2bda0000000p-3, -0x1.34b4ca0000000p-8}
, {0x1.97b5f20000000p-2, 0x1.3e216a0000000p-3, 0x1.5e11960000000p-4, -0x1.e677e60000000p-3, 0x1.353fde0000000p-3, 0x1.310fc00000000p-2, -0x1.9a8b9e0000000p-4, -0x1.a5c57c0000000p-3}
, {0x1.0d192a0000000p-4, 0x1.293b340000000p-4, 0x1.c8a2600000000p-3, -0x1.47713a0000000p-3, 0x1.ce74820000000p-3, -0x1.ce413a0000000p-6, -0x1.ed6a260000000p-3, -0x1.4df9940000000p-3}
}
, {{-0x1.81ccb40000000p-3, 0x1.9e957c0000000p-8, -0x1.543af00000000p-5, -0x1.1ccd700000000p-6, -0x1.e3b4820000000p-6, -0x1.d93f460000000p-5, -0x1.3e42160000000p-5, -0x1.dbb7480000000p-3}
, {-0x1.0b7d140000000p-5, 0x1.e487180000000p-6, 0x1.0412c60000000p-4, -0x1.c473660000000p-3, -0x1.c5d61a0000000p-5, 0x1.298ab40000000p-5, -0x1.6a88f20000000p-3, 0x1.201d900000000p-10}
, {-0x1.1996580000000p-2, -0x1.a3fe8e0000000p-3, -0x1.0253fe0000000p-5, -0x1.54a1200000000p-8, -0x1.e1c1580000000p-3, -0x1.f4e4540000000p-3, -0x1.946b460000000p-3, 0x1.798f4a0000000p-5}
}
, {{-0x1.44d3020000000p-2, 0x1.25b19e0000000p-3, -0x1.cf39760000000p-6, 0x1.dd11660000000p-3, 0x1.1ef6360000000p-3, 0x1.1898aa0000000p-4, -0x1.77327a0000000p-2, -0x1.d6bdc00000000p-3}
, {0x1.56a7c00000000p-3, 0x1.fb8b860000000p-5, 0x1.9107080000000p-3, -0x1.d2fab00000000p-5, 0x1.94455e0000000p-4, -0x1.1efac80000000p-1, -0x1.14095a0000000p-4, -0x1.a36cac0000000p-3}
, {0x1.8d45940000000p-2, 0x1.10fe580000000p-2, -0x1.3f9e4c0000000p-4, 0x1.0239400000000p-2, 0x1.a0601c0000000p-4, -0x1.0739b60000000p-4, 0x1.098d8c0000000p-2, -0x1.3bf4e40000000p-4}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    maxpool1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _MAX_POOLING1D_1_H_
#define _MAX_POOLING1D_1_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   128
#define POOL_SIZE       2
#define POOL_STRIDE     2
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

typedef float max_pooling1d_1_output_type[POOL_LENGTH][INPUT_CHANNELS];

#if 0
void max_pooling1d_1(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  number_t output[POOL_LENGTH][INPUT_CHANNELS]); 	// OUT
#endif

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH

#endif//_MAX_POOLING1D_1_H_
/**
  ******************************************************************************
  * @file    maxpool.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "max_pooling1d_1.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   128
#define POOL_SIZE       2
#define POOL_STRIDE     2
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void max_pooling1d_1(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  NUMBER_T output[POOL_LENGTH][INPUT_CHANNELS]) {	// OUT

  unsigned short pos_x, k; 	// loop indexes for output volume
  unsigned int x;
  static LONG_NUMBER_T max[INPUT_CHANNELS];

  for (pos_x = 0; pos_x < POOL_LENGTH; pos_x++) {
    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef ACTIVATION_LINEAR
      max[k] = input[pos_x*POOL_STRIDE][k];
      x = 1;
#elif defined(ACTIVATION_RELU)
      max[k] = 0;
      x = 0;
#endif
    }

    for (; x < POOL_SIZE; x++) {
      for (k = 0; k < INPUT_CHANNELS; k++) {
        if (max[k] < input[(pos_x * POOL_STRIDE) + x][k])
          max[k] = input[(pos_x * POOL_STRIDE) + x][k];
      }
    }

    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef WITH_CMSIS_NN
// Not really CMSIS-NN since using arm_relu_q* is not more efficient, but use SSAT anyway
#if ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR > 0
      output[pos_x][k] = __SSAT(max[k] >> (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#else
      output[pos_x][k] = __SSAT(max[k] << (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#endif
#else
      max[k] = scale(NUMBER_T, max[k], INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, max[k]);
#endif
    }
  }
}

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH
#undef ACTIVATION_LINEAR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    operator.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _ADD_H_
#define _ADD_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

typedef float add_output_type[64][8];

#if 0
void add(

  const number_t vector_in_1[64][8], // doesn't work with inverted data_format

  const number_t vector_in_2[64][8], // doesn't work with inverted data_format

  add_output_type vector_out);     // OUT
#endif

#endif//_ADD_H_
/**
  ******************************************************************************
  * @file    operator.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "add.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#endif

#define ACTIVATION_RELU

// For fixed point quantization
#define ACC_SCALE_FACTOR 0 // Get maximum scale factor of previous layers
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float

static inline void add(

  const NUMBER_T vector_in_1[64][8], // doesn't work with inverted data_format

  const NUMBER_T vector_in_2[64][8], // doesn't work with inverted data_format

  add_output_type vector_out) {    // OUT

  size_t x;
  LONG_NUMBER_T output_acc;


  NUMBER_T *i_1 = (NUMBER_T*)vector_in_1;

  NUMBER_T *i_2 = (NUMBER_T*)vector_in_2;


  NUMBER_T *o = (NUMBER_T*)vector_out;

  for (x = 0; x < 64*8; x++) {
    // scale all fixed point inputs to same factor and add them, negative factor is left shift
    output_acc = 
                    + scale(NUMBER_T, (LONG_NUMBER_T)i_1[x], 0 - ACC_SCALE_FACTOR)
                 
                    + scale(NUMBER_T, (LONG_NUMBER_T)i_2[x], 0 - ACC_SCALE_FACTOR)
                 ;
#ifdef ACTIVATION_LINEAR
    output_acc = scale(NUMBER_T, output_acc, ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
    o[x] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
    if (output_acc < 0) {
      o[x] = 0;
    } else {
#ifdef WITH_CMSIS_NN
// Not really CMSIS-NN since using arm_relu_q* is not more efficient, but use SSAT anyway
#if ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR > 0
      o[x] = __SSAT(output_acc >> (ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#else
      o[x] = __SSAT(output_acc << (ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#endif
#else
      output_acc = scale(NUMBER_T, output_acc, ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      o[x] = clamp_to(NUMBER_T, output_acc);
#endif
    }
#endif
  }
}

#undef ACTIVATION_RELU
#undef ACC_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV1D_2_H_
#define _CONV1D_2_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv1d_2_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv1d_2(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV1D_2_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv1d_2.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_RELU

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv1d_2(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_RELU
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    8
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  3


const float  conv1d_2_bias[CONV_FILTERS] = {0x1.6664a40000000p-4, 0x1.69cea80000000p-2, 0x1.12118a0000000p-7, -0x1.70ed240000000p-2, 0x1.e439b00000000p-1, -0x1.1c069c0000000p-4, 0x1.d3393e0000000p-1, 0x1.69d1c80000000p-1}
;

const float  conv1d_2_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{0x1.84e15e0000000p-2, 0x1.72c93c0000000p-3, -0x1.62c1400000000p-3, -0x1.44a2fe0000000p-2, -0x1.8e3c7e0000000p-2, -0x1.a800320000000p-2, 0x1.21393a0000000p-3, 0x1.26ddd80000000p-3}
, {0x1.1a0e5a0000000p-2, 0x1.6a79d80000000p-2, 0x1.7cd29e0000000p-4, -0x1.8755fa0000000p-2, 0x1.257c2a0000000p-6, -0x1.594a6e0000000p-2, 0x1.d2f78c0000000p-4, 0x1.e7115c0000000p-9}
, {-0x1.13d9e40000000p-4, 0x1.adb0240000000p-5, -0x1.120d6a0000000p-3, 0x1.607c5c0000000p-3, 0x1.1d795e0000000p-2, -0x1.44909e0000000p-1, -0x1.5b6a680000000p-5, -0x1.319cc40000000p-4}
}
, {{0x1.d8383a0000000p-4, 0x1.44663a0000000p-2, 0x1.e925960000000p-3, -0x1.046fe60000000p-3, 0x1.85c5300000000p-3, -0x1.c15c340000000p-3, -0x1.1dc8f60000000p-4, 0x1.1001440000000p-2}
, {0x1.65fd9e0000000p-5, 0x1.15d5ea0000000p-2, 0x1.3437ee0000000p-2, 0x1.3d69680000000p-3, 0x1.0e503a0000000p-1, 0x1.17c0440000000p-3, -0x1.8978e60000000p-4, 0x1.aa73c20000000p-5}
, {-0x1.47034a0000000p-2, -0x1.548db20000000p-4, 0x1.8571580000000p-3, -0x1.0da4960000000p-9, -0x1.6f0cd60000000p-7, -0x1.d477cc0000000p-3, 0x1.dbaa400000000p-8, -0x1.bf0e400000000p-4}
}
, {{-0x1.0460940000000p-2, -0x1.8e77fc0000000p-2, 0x1.113f780000000p-1, 0x1.e16a900000000p-3, 0x1.19da600000000p-2, 0x1.fc69ac0000000p-3, -0x1.b235ec0000000p-4, 0x1.e174d00000000p-4}
, {-0x1.a0b6fe0000000p-3, -0x1.6e2fc20000000p-2, 0x1.7388440000000p-3, -0x1.2700f20000000p-2, -0x1.c0bff60000000p-2, -0x1.6404700000000p-3, 0x1.acb9900000000p-4, 0x1.d7a7b00000000p-2}
, {0x1.c241d80000000p-4, -0x1.0c17c60000000p-3, -0x1.cbd0520000000p-3, -0x1.37a23c0000000p-1, -0x1.bafd500000000p-2, 0x1.2521680000000p-2, 0x1.c31d580000000p-5, 0x1.1b1cca0000000p-3}
}
, {{0x1.ddee280000000p-6, 0x1.d537e00000000p-4, 0x1.7e240c0000000p-2, -0x1.e26bf00000000p-9, 0x1.f9c17e0000000p-4, 0x1.2d09d20000000p-9, 0x1.0415200000000p-2, -0x1.95c48a0000000p-7}
, {0x1.3130660000000p-5, 0x1.a3946c0000000p-3, 0x1.11c5fa0000000p-2, -0x1.3197000000000p-3, 0x1.a2b76e0000000p-4, 0x1.3a744a0000000p-6, 0x1.fbb1420000000p-3, -0x1.76998e0000000p-12}
, {-0x1.1030ec0000000p-3, -0x1.690a580000000p-4, 0x1.eb34ac0000000p-5, -0x1.3637d40000000p-2, 0x1.5602b60000000p-2, -0x1.40d95a0000000p-3, 0x1.2832d20000000p-3, 0x1.1f1c8c0000000p-2}
}
, {{-0x1.5678ec0000000p-4, -0x1.792a020000000p-2, -0x1.3ea9c40000000p-1, -0x1.31b7040000000p-3, -0x1.20cbc00000000p-1, 0x1.626f1e0000000p-2, 0x1.2cbaa60000000p-4, -0x1.17487c0000000p-1}
, {0x1.77d6020000000p-6, -0x1.2901da0000000p-2, -0x1.99157c0000000p-2, -0x1.4451c00000000p-3, -0x1.232c600000000p-2, 0x1.7852720000000p-4, -0x1.81640a0000000p-3, -0x1.6781e60000000p-2}
, {0x1.758fd20000000p-3, -0x1.5937a40000000p-2, 0x1.ee65060000000p-6, -0x1.9e2cb40000000p-8, -0x1.70a03c0000000p-3, -0x1.5a65980000000p-5, -0x1.6f8cc40000000p-7, -0x1.6f87120000000p-4}
}
, {{-0x1.18185a0000000p-2, -0x1.fda0120000000p-2, 0x1.0103ca0000000p-2, -0x1.98f4bc0000000p-5, 0x1.7528d80000000p-3, 0x1.3063fc0000000p-2, 0x1.31fd620000000p-4, -0x1.43b48e0000000p-2}
, {-0x1.187c420000000p-2, -0x1.865a620000000p-4, -0x1.8ce3360000000p-6, 0x1.3560420000000p-4, 0x1.b63dbc0000000p-4, 0x1.68b7700000000p-4, -0x1.8b7e5a0000000p-3, -0x1.3b19bc0000000p-3}
, {-0x1.ad0bfc0000000p-6, 0x1.09b0340000000p-2, -0x1.b88cdc0000000p-4, -0x1.b6a49e0000000p-10, 0x1.5b69900000000p-3, 0x1.de8d540000000p-5, -0x1.e12e5e0000000p-3, 0x1.8a920a0000000p-2}
}
, {{-0x1.39cede0000000p-2, -0x1.67283c0000000p-3, 0x1.1ca9b00000000p-4, -0x1.ec0eee0000000p-3, -0x1.6af5f80000000p-2, 0x1.bc2c7a0000000p-4, -0x1.dcdf6c0000000p-6, -0x1.c9317a0000000p-3}
, {0x1.dcc0a20000000p-4, 0x1.6eceea0000000p-3, 0x1.16bc160000000p-5, -0x1.fc1d8a0000000p-5, 0x1.e2e2c00000000p-3, -0x1.32610c0000000p-2, 0x1.1f52c80000000p-4, 0x1.0e48640000000p-3}
, {0x1.34c5080000000p-5, 0x1.fb48820000000p-3, 0x1.e859240000000p-4, 0x1.0e45520000000p-3, 0x1.6e7e0e0000000p-2, -0x1.d3627e0000000p-2, -0x1.b715460000000p-3, -0x1.0d363e0000000p-6}
}
, {{-0x1.4104980000000p-3, -0x1.56b6300000000p-2, -0x1.188df60000000p-2, -0x1.f7734a0000000p-3, -0x1.7f68260000000p-2, 0x1.b51aaa0000000p-2, -0x1.2a748e0000000p-4, 0x1.6d59140000000p-2}
, {-0x1.e0cba80000000p-3, 0x1.abad760000000p-9, 0x1.0eaf540000000p-3, -0x1.6da5640000000p-2, 0x1.6896c60000000p-2, 0x1.fac93e0000000p-2, -0x1.c7a9cc0000000p-7, 0x1.d552d60000000p-3}
, {0x1.ca8df80000000p-3, 0x1.87a49e0000000p-5, -0x1.858b2c0000000p-2, -0x1.3badb60000000p-5, 0x1.2bb0960000000p-4, -0x1.f215200000000p-2, -0x1.664f800000000p-3, -0x1.bfa9d80000000p-4}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    conv1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _CONV_REF_1_H_
#define _CONV_REF_1_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

typedef float conv_ref_1_output_type[CONV_OUTSAMPLES][CONV_FILTERS];

#if 0
void conv_ref_1(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const number_t kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const number_t bias[CONV_FILTERS],						                          // IN

  number_t output[CONV_OUTSAMPLES][CONV_FILTERS]);                       // OUT
#endif

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES

#endif//_CONV_REF_1_H_
/**
  ******************************************************************************
  * @file    conv.cc
  * @author  Sébastien Bilavarn, LEAT, CNRS, Université Côte d'Azur, France
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "conv_ref_1.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_CHANNELS      8
#define INPUT_SAMPLES       64
#define CONV_FILTERS        8
#define CONV_KERNEL_SIZE    3
#define CONV_STRIDE         1

#define ZEROPADDING_LEFT    1
#define ZEROPADDING_RIGHT   1

#define CONV_OUTSAMPLES     ( ( (INPUT_SAMPLES - CONV_KERNEL_SIZE + ZEROPADDING_LEFT + ZEROPADDING_RIGHT) / CONV_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void conv_ref_1(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS],                    // IN
  const NUMBER_T kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS],  // IN

  const NUMBER_T bias[CONV_FILTERS],						                          // IN

  NUMBER_T output[CONV_OUTSAMPLES][CONV_FILTERS]) {                       // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short pos_x, z, k; 	// loop indexes for output volume
  unsigned short x;
  int input_x;
  LONG_NUMBER_T output_acc;

  for (pos_x = 0; pos_x < CONV_OUTSAMPLES; pos_x++) { 
    for (k = 0; k < CONV_FILTERS; k++) { 

      output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);


      for (x = 0; x < CONV_KERNEL_SIZE; x++) {
        input_x = pos_x * CONV_STRIDE - ZEROPADDING_LEFT + x;

        if (input_x >= 0 && input_x < INPUT_SAMPLES) { // ZeroPadding1D
          for (z = 0; z < INPUT_CHANNELS; z++) {
            output_acc += (LONG_NUMBER_T)input[input_x][z] * (LONG_NUMBER_T)kernel[k][x][z];
          }
        }
      }
      
#ifdef ACTIVATION_LINEAR
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
      // Activation function: ReLU
      if (output_acc < 0) {
        output[pos_x][k] = 0;
      } else {
        output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
        output[pos_x][k] = clamp_to(NUMBER_T, output_acc);
      }
#endif
    }
  }

#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_CHANNELS
#undef INPUT_SAMPLES
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
#undef CONV_STRIDE
#undef ZEROPADDING_LEFT
#undef ZEROPADDING_RIGHT
#undef CONV_OUTSAMPLES
#undef ACTIVATION_LINEAR
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/conv1d.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_CHANNELS    8
#define CONV_FILTERS      8
#define CONV_KERNEL_SIZE  3


const float  conv_ref_1_bias[CONV_FILTERS] = {0x1.08db440000000p-3, -0x1.bb2bfe0000000p-6, -0x1.c4a7440000000p-6, -0x1.0514600000000p-3, 0x1.b491ba0000000p-3, 0x1.0156d40000000p-2, 0x1.7a9ed80000000p-1, -0x1.a315380000000p-3}
;

const float  conv_ref_1_kernel[CONV_FILTERS][CONV_KERNEL_SIZE][INPUT_CHANNELS] = {{{0x1.54cbba0000000p-3, 0x1.7cf5200000000p-3, -0x1.1690ea0000000p-7, 0x1.0e83e60000000p-3, 0x1.c8c42c0000000p-3, 0x1.545f380000000p-3, -0x1.f3d0880000000p-3, -0x1.29f45a0000000p-1}
, {0x1.2204840000000p-7, -0x1.db3cee0000000p-7, -0x1.2093620000000p-2, 0x1.484e280000000p-3, 0x1.0e60f80000000p-2, 0x1.2e8a4a0000000p-2, -0x1.c2b7800000000p-6, -0x1.4cc5660000000p-6}
, {0x1.e2c51c0000000p-4, -0x1.d4d8f80000000p-3, -0x1.6429040000000p-4, -0x1.7597020000000p-5, 0x1.7a223e0000000p-2, -0x1.824c560000000p-2, 0x1.4c5b420000000p-5, 0x1.9aa9820000000p-3}
}
, {{0x1.5ee5e40000000p-3, -0x1.f91ada0000000p-4, -0x1.c7df700000000p-3, 0x1.476b8a0000000p-3, 0x1.6ec3ca0000000p-2, -0x1.72e5e80000000p-4, 0x1.655c800000000p-3, 0x1.082e020000000p-1}
, {0x1.03cad80000000p-2, -0x1.868e540000000p-3, -0x1.c442860000000p-2, 0x1.4542dc0000000p-3, -0x1.a3a4400000000p-4, 0x1.778dd60000000p-6, 0x1.35d83c0000000p-2, -0x1.edb6020000000p-5}
, {0x1.a4fb4e0000000p-3, 0x1.2a32900000000p-3, -0x1.31bda20000000p-1, -0x1.8f18e00000000p-3, 0x1.dc2fce0000000p-4, -0x1.3704560000000p-1, 0x1.53fff40000000p-2, -0x1.2c4b540000000p-3}
}
, {{0x1.d8d8200000000p-4, 0x1.126c2a0000000p-2, 0x1.e6ea800000000p-4, 0x1.d786920000000p-3, -0x1.867cdc0000000p-4, -0x1.6e59ac0000000p-3, -0x1.3902e20000000p-3, -0x1.ea62de0000000p-3}
, {-0x1.80db200000000p-3, 0x1.8001660000000p-2, -0x1.1fa9ae0000000p-6, -0x1.9df8e80000000p-6, -0x1.4e33ac0000000p-2, -0x1.94293e0000000p-3, -0x1.02342c0000000p-3, -0x1.f838980000000p-5}
, {0x1.8ed6340000000p-11, -0x1.3894500000000p-4, 0x1.1087a00000000p-4, 0x1.1fd7820000000p-6, -0x1.da86bc0000000p-4, -0x1.39a3ee0000000p-4, -0x1.bffa7c0000000p-6, -0x1.3e59680000000p-2}
}
, {{-0x1.1eea080000000p-3, 0x1.4161a20000000p-3, -0x1.4e84c00000000p-1, 0x1.cd01940000000p-7, -0x1.ca5a2c0000000p-5, 0x1.d820c60000000p-2, -0x1.1a548c0000000p-3, 0x1.c9b93c0000000p-2}
, {0x1.3278b40000000p-4, 0x1.5e286e0000000p-2, -0x1.d746320000000p-2, 0x1.21836a0000000p-4, -0x1.b48db20000000p-2, 0x1.375c2a0000000p-5, 0x1.d14ad80000000p-3, -0x1.0ab5840000000p-3}
, {0x1.786c440000000p-4, 0x1.935cac0000000p-4, 0x1.ceb4040000000p-4, -0x1.975e020000000p-4, 0x1.4a530a0000000p-5, -0x1.6431fc0000000p-5, -0x1.6af88a0000000p-2, -0x1.32e0ce0000000p-3}
}
, {{-0x1.e2f4c80000000p-5, -0x1.d08aba0000000p-3, 0x1.8a4c140000000p-3, -0x1.0f6c6a0000000p-3, 0x1.1b20800000000p-1, -0x1.eca62c0000000p-4, -0x1.4502a60000000p-3, 0x1.07b33e0000000p-2}
, {-0x1.e329c40000000p-2, 0x1.c63f180000000p-7, -0x1.e91b900000000p-4, -0x1.44aee80000000p-2, 0x1.7723920000000p-2, -0x1.848d1c0000000p-3, -0x1.bb93040000000p-3, 0x1.45cf940000000p-1}
, {-0x1.0f23360000000p-2, -0x1.9218520000000p-5, 0x1.7685c40000000p-4, -0x1.46e2f80000000p-3, 0x1.a3e64c0000000p-5, 0x1.5da4200000000p-3, -0x1.1f7c960000000p-1, 0x1.d4b02c0000000p-5}
}
, {{-0x1.38f3fc0000000p-2, 0x1.a6ca720000000p-2, 0x1.59dcbc0000000p-4, 0x1.2d8f940000000p-7, 0x1.b9f1ea0000000p-3, 0x1.78cbde0000000p-2, 0x1.d881000000000p-3, 0x1.11d2900000000p-4}
, {-0x1.4cb2fa0000000p-3, 0x1.3b67020000000p-2, 0x1.5159660000000p-2, 0x1.69644e0000000p-4, 0x1.e4e1960000000p-4, 0x1.c0d6420000000p-4, 0x1.c612d40000000p-2, 0x1.314ac40000000p-2}
, {-0x1.1577600000000p-3, -0x1.547e7e0000000p-3, 0x1.d727fe0000000p-4, -0x1.8c94560000000p-5, -0x1.3b40460000000p-2, -0x1.6221420000000p-4, -0x1.775e9e0000000p-1, -0x1.ccc16e0000000p-4}
}
, {{0x1.82d9460000000p-5, -0x1.257b1c0000000p-1, 0x1.5eea720000000p-3, -0x1.ec65720000000p-5, -0x1.9efe6a0000000p-2, 0x1.6c28ae0000000p-2, -0x1.a082dc0000000p-3, -0x1.7f3fc80000000p-2}
, {0x1.69558e0000000p-4, 0x1.4695e80000000p-4, 0x1.e1905a0000000p-3, -0x1.42bea00000000p-2, 0x1.ccb4360000000p-2, -0x1.b813400000000p-4, 0x1.10e8460000000p-1, 0x1.1167840000000p-1}
, {0x1.3461720000000p-3, 0x1.cc569c0000000p-2, -0x1.86cf260000000p-3, -0x1.1d09980000000p-2, 0x1.058fde0000000p-1, -0x1.af6b7a0000000p-4, 0x1.d919760000000p-2, 0x1.fc9b020000000p-3}
}
, {{-0x1.8fbb8a0000000p-1, -0x1.083be00000000p-2, 0x1.d67b9a0000000p-2, 0x1.2b68ca0000000p-3, 0x1.01bc460000000p-3, 0x1.486ba20000000p-2, 0x1.8b3f4e0000000p-2, 0x1.d7dd480000000p-4}
, {-0x1.4a4cac0000000p-3, -0x1.3c527e0000000p-2, 0x1.d0496e0000000p-2, -0x1.811d340000000p-4, -0x1.6d3fb40000000p-1, 0x1.a903540000000p-2, 0x1.15a66a0000000p-2, 0x1.3b7f360000000p-5}
, {0x1.4399ca0000000p-2, 0x1.50522a0000000p-3, -0x1.7b1a3a0000000p-2, -0x1.56eef20000000p-3, -0x1.139c480000000p-1, -0x1.9a8a8a0000000p-3, 0x1.921dbe0000000p-8, 0x1.14d7ce0000000p-2}
}
}
;

#undef INPUT_CHANNELS
#undef CONV_FILTERS
#undef CONV_KERNEL_SIZE
/**
  ******************************************************************************
  * @file    operator.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _ADD_1_H_
#define _ADD_1_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

typedef float add_1_output_type[64][8];

#if 0
void add_1(

  const number_t vector_in_1[64][8], // doesn't work with inverted data_format

  const number_t vector_in_2[64][8], // doesn't work with inverted data_format

  add_1_output_type vector_out);     // OUT
#endif

#endif//_ADD_1_H_
/**
  ******************************************************************************
  * @file    operator.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "add_1.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#endif

#define ACTIVATION_RELU

// For fixed point quantization
#define ACC_SCALE_FACTOR 0 // Get maximum scale factor of previous layers
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float

static inline void add_1(

  const NUMBER_T vector_in_1[64][8], // doesn't work with inverted data_format

  const NUMBER_T vector_in_2[64][8], // doesn't work with inverted data_format

  add_1_output_type vector_out) {    // OUT

  size_t x;
  LONG_NUMBER_T output_acc;


  NUMBER_T *i_1 = (NUMBER_T*)vector_in_1;

  NUMBER_T *i_2 = (NUMBER_T*)vector_in_2;


  NUMBER_T *o = (NUMBER_T*)vector_out;

  for (x = 0; x < 64*8; x++) {
    // scale all fixed point inputs to same factor and add them, negative factor is left shift
    output_acc = 
                    + scale(NUMBER_T, (LONG_NUMBER_T)i_1[x], 0 - ACC_SCALE_FACTOR)
                 
                    + scale(NUMBER_T, (LONG_NUMBER_T)i_2[x], 0 - ACC_SCALE_FACTOR)
                 ;
#ifdef ACTIVATION_LINEAR
    output_acc = scale(NUMBER_T, output_acc, ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
    o[x] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
    if (output_acc < 0) {
      o[x] = 0;
    } else {
#ifdef WITH_CMSIS_NN
// Not really CMSIS-NN since using arm_relu_q* is not more efficient, but use SSAT anyway
#if ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR > 0
      o[x] = __SSAT(output_acc >> (ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#else
      o[x] = __SSAT(output_acc << (ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#endif
#else
      output_acc = scale(NUMBER_T, output_acc, ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      o[x] = clamp_to(NUMBER_T, output_acc);
#endif
    }
#endif
  }
}

#undef ACTIVATION_RELU
#undef ACC_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    maxpool1d.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _MAX_POOLING1D_2_H_
#define _MAX_POOLING1D_2_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   64
#define POOL_SIZE       64
#define POOL_STRIDE     64
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

typedef float max_pooling1d_2_output_type[POOL_LENGTH][INPUT_CHANNELS];

#if 0
void max_pooling1d_2(
  const number_t input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  number_t output[POOL_LENGTH][INPUT_CHANNELS]); 	// OUT
#endif

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH

#endif//_MAX_POOLING1D_2_H_
/**
  ******************************************************************************
  * @file    maxpool.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "max_pooling1d_2.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#endif

#define INPUT_CHANNELS  8
#define INPUT_SAMPLES   64
#define POOL_SIZE       64
#define POOL_STRIDE     64
#define POOL_PAD        0 // Unsupported
#define POOL_LENGTH	    ( ( (INPUT_SAMPLES - POOL_SIZE + (2*POOL_PAD) ) / POOL_STRIDE ) + 1 )

#define ACTIVATION_LINEAR

// For fixed point quantization
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void max_pooling1d_2(
  const NUMBER_T input[INPUT_SAMPLES][INPUT_CHANNELS], 	    // IN
  NUMBER_T output[POOL_LENGTH][INPUT_CHANNELS]) {	// OUT

  unsigned short pos_x, k; 	// loop indexes for output volume
  unsigned int x;
  static LONG_NUMBER_T max[INPUT_CHANNELS];

  for (pos_x = 0; pos_x < POOL_LENGTH; pos_x++) {
    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef ACTIVATION_LINEAR
      max[k] = input[pos_x*POOL_STRIDE][k];
      x = 1;
#elif defined(ACTIVATION_RELU)
      max[k] = 0;
      x = 0;
#endif
    }

    for (; x < POOL_SIZE; x++) {
      for (k = 0; k < INPUT_CHANNELS; k++) {
        if (max[k] < input[(pos_x * POOL_STRIDE) + x][k])
          max[k] = input[(pos_x * POOL_STRIDE) + x][k];
      }
    }

    for (k = 0; k < INPUT_CHANNELS; k++) {
#ifdef WITH_CMSIS_NN
// Not really CMSIS-NN since using arm_relu_q* is not more efficient, but use SSAT anyway
#if ACC_SCALE_FACTOR - OUTPUT_SCALE_FACTOR > 0
      output[pos_x][k] = __SSAT(max[k] >> (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#else
      output[pos_x][k] = __SSAT(max[k] << (INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR), sizeof(NUMBER_T) * 8);
#endif
#else
      max[k] = scale(NUMBER_T, max[k], INPUT_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[pos_x][k] = clamp_to(NUMBER_T, max[k]);
#endif
    }
  }
}

#undef INPUT_CHANNELS  
#undef INPUT_SAMPLES
#undef POOL_SIZE
#undef POOL_STRIDE
#undef POOL_PAD
#undef POOL_LENGTH
#undef ACTIVATION_LINEAR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    flatten.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _FLATTEN_H_
#define _FLATTEN_H_

#ifndef SINGLE_FILE
#include "number.h"
#endif

#define OUTPUT_DIM 8

typedef float flatten_output_type[OUTPUT_DIM];

#if 0
void flatten(
  const number_t input[1][8], 			      // IN
	number_t output[OUTPUT_DIM]); 			                // OUT
#endif

#undef OUTPUT_DIM

#endif//_FLATTEN_H_
/**
  ******************************************************************************
  * @file    flatten.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 2.0.0
  * @date    26 november 2021
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "flatten.h"
#include "number.h"
#endif

#define OUTPUT_DIM 8

#define NUMBER_T float
#define LONG_NUMBER_T float

static inline void flatten(
  const NUMBER_T input[1][8], 			      // IN
	NUMBER_T output[OUTPUT_DIM]) {			                // OUT

  NUMBER_T *input_flat = (NUMBER_T *)input;

  // Copy data from input to output only if input and output don't point to the same memory address already
  if (input_flat != output) {
    for (size_t i = 0; i < OUTPUT_DIM; i++) {
      output[i] = input_flat[i];
    }
  }
}

#undef OUTPUT_DIM
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    fc.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version V2.0
  * @date    24 january 2023
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef _DENSE_H_
#define _DENSE_H_

#ifndef SINGLE_FILE
#include "number.h"
#include <stdint.h>
#endif

#define INPUT_SAMPLES 8
#define FC_UNITS 6

typedef float dense_output_type[FC_UNITS];

#if 0
void dense(
  const number_t input[INPUT_SAMPLES], 			      // IN
	const number_t kernel[FC_UNITS][INPUT_SAMPLES],  // IN

	const number_t bias[FC_UNITS],			              // IN

	number_t output[FC_UNITS]); 			                // OUT
#endif

#undef INPUT_SAMPLES
#undef FC_UNITS

#endif//_DENSE_H_
/**
  ******************************************************************************
  * @file    fc.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifndef SINGLE_FILE
#include "dense.h"
#include "number.h"
#endif

#ifdef WITH_CMSIS_NN
#include "arm_nnfunctions.h"
#elif defined(WITH_NMSIS_NN)
#include "riscv_nnfunctions.h"
#endif

#define INPUT_SAMPLES 8
#define FC_UNITS 6
#define ACTIVATION_LINEAR

// For fixed point quantization
#define WEIGHTS_SCALE_FACTOR 0
#define INPUT_SCALE_FACTOR 0
#define OUTPUT_SCALE_FACTOR 0
#define NUMBER_T float
#define LONG_NUMBER_T float


static inline void dense(
  const NUMBER_T input[INPUT_SAMPLES], 			      // IN
	const NUMBER_T kernel[FC_UNITS][INPUT_SAMPLES],  // IN

	const NUMBER_T bias[FC_UNITS],			              // IN

	NUMBER_T output[FC_UNITS]) {			                // OUT

#if !defined(WITH_CMSIS_NN) && !defined(WITH_NMSIS_NN)
  unsigned short k, z; 
  LONG_NUMBER_T output_acc;

  for (k = 0; k < FC_UNITS; k++) { 

    output_acc = scale(NUMBER_T, (LONG_NUMBER_T)bias[k], -INPUT_SCALE_FACTOR);

    for (z = 0; z < INPUT_SAMPLES; z++) 
      output_acc = output_acc + ((LONG_NUMBER_T)kernel[k][z] * (LONG_NUMBER_T)input[z]);

    // Activation function
#ifdef ACTIVATION_LINEAR
    // Linear (MEANS NONE)
    output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
    output[k] = clamp_to(NUMBER_T, output_acc);
#elif defined(ACTIVATION_RELU)
    // ReLU
    if (output_acc < 0) {
      output[k] = 0;
    } else {
      output_acc = scale(NUMBER_T, output_acc, INPUT_SCALE_FACTOR + WEIGHTS_SCALE_FACTOR - OUTPUT_SCALE_FACTOR);
      output[k] = clamp_to(NUMBER_T, output_acc);
    }
#endif
  }
#else


#error "Data type unsupported by CMSIS-NN"

#endif
}

#undef INPUT_SAMPLES
#undef FC_UNITS
#undef ACTIVATION_LINEAR
#undef WEIGHTS_SCALE_FACTOR
#undef INPUT_SCALE_FACTOR
#undef OUTPUT_SCALE_FACTOR
#undef NUMBER_T
#undef LONG_NUMBER_T
/**
  ******************************************************************************
  * @file    weights/fc.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#include <stdint.h>

#define INPUT_SAMPLES 8
#define FC_UNITS 6


const float dense_bias[FC_UNITS] = {-0x1.6c0e120000000p-2, -0x1.70fcd80000000p-2, -0x1.ebcfde0000000p-2, 0x1.8064440000000p-2, 0x1.5494820000000p-1, 0x1.405c5a0000000p-5}
;

const float dense_kernel[FC_UNITS][INPUT_SAMPLES] = {{-0x1.2ca39e0000000p-5, 0x1.c36d0c0000000p-8, 0x1.b2d8fa0000000p-6, -0x1.2877be0000000p-3, -0x1.0cb3720000000p-2, -0x1.8e23d60000000p-4, -0x1.1a04bc0000000p-3, 0x1.64ae840000000p-2}
, {0x1.181e1e0000000p-1, -0x1.7fd4540000000p-3, 0x1.94284e0000000p-5, 0x1.f5f4880000000p-3, -0x1.ae3ed00000000p-2, 0x1.bdedf60000000p-4, -0x1.1153280000000p-1, -0x1.c59cde0000000p-3}
, {-0x1.3cf1340000000p-2, 0x1.11deba0000000p-1, 0x1.893bc40000000p-3, 0x1.3704ac0000000p-2, -0x1.4ae8980000000p-5, -0x1.4d4ee60000000p-3, -0x1.bee80c0000000p-2, -0x1.a579280000000p-3}
, {-0x1.72f0660000000p-3, 0x1.73473a0000000p-4, -0x1.3625e80000000p-2, -0x1.7bec2a0000000p-2, 0x1.5450780000000p-2, 0x1.6da72c0000000p-1, 0x1.f3240e0000000p-4, -0x1.420c300000000p-2}
, {-0x1.1388d20000000p-5, 0x1.d1f86a0000000p-4, -0x1.984d0c0000000p-4, -0x1.95a0740000000p-2, -0x1.d55d500000000p-2, 0x1.5be4300000000p-3, 0x1.6c99ce0000000p-1, -0x1.03bbc40000000p-1}
, {-0x1.6104700000000p-3, -0x1.aec4c00000000p-3, 0x1.64c99c0000000p-1, -0x1.ea75ca0000000p-3, -0x1.2c0f280000000p-2, 0x1.3640600000000p-2, -0x1.0e54f40000000p-3, -0x1.39b7ee0000000p-4}
}
;

#undef INPUT_SAMPLES
#undef FC_UNITS
/**
  ******************************************************************************
  * @file    model.hh
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    08 july 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */


#ifdef __cplusplus
extern "C" {
#endif

#ifndef __MODEL_H__
#define __MODEL_H__

#ifndef SINGLE_FILE
#include "number.h"

 // InputLayer is excluded
#include "conv1d.h" // InputLayer is excluded
#include "conv1d_1.h" // InputLayer is excluded
#include "max_pooling1d.h" // InputLayer is excluded
#include "conv_shortcut.h" // InputLayer is excluded
#include "conv_ref.h" // InputLayer is excluded
#include "max_pooling1d_1.h" // InputLayer is excluded
#include "add.h" // InputLayer is excluded
#include "conv1d_2.h" // InputLayer is excluded
#include "conv_ref_1.h" // InputLayer is excluded
#include "add_1.h" // InputLayer is excluded
#include "max_pooling1d_2.h" // InputLayer is excluded
#include "flatten.h" // InputLayer is excluded
#include "dense.h"
#endif


#define MODEL_INPUT_DIM_0 128
#define MODEL_INPUT_DIM_1 9
#define MODEL_INPUT_DIMS 128 * 9

#define MODEL_OUTPUT_SAMPLES 6

#define MODEL_INPUT_SCALE_FACTOR 0 // scale factor of InputLayer
#define MODEL_INPUT_NUMBER_T float
#define MODEL_INPUT_LONG_NUMBER_T float

// node 0 is InputLayer so use its output shape as input shape of the model
// typedef  input_t[128][9];
typedef float input_t[128][9];
typedef dense_output_type output_t;


void cnn(
  const input_t input,
  output_t output);

void reset(void);

#endif//__MODEL_H__


#ifdef __cplusplus
} // extern "C"
#endif
/**
  ******************************************************************************
  * @file    model.cc
  * @author  Pierre-Emmanuel Novac <penovac@unice.fr>, LEAT, CNRS, Université Côte d'Azur, France
  * @version 1.0.0
  * @date    24 march 2020
  * @brief   Template generating plain C code for the implementation of Convolutional Neural Networks on MCU
  */

#ifdef __cplusplus
extern "C" {
#endif

#ifndef SINGLE_FILE
#include "number.h"
#include "model.h"
// #include <chrono>

 // InputLayer is excluded
#include "conv1d.c"
#include "weights/conv1d.c" // InputLayer is excluded
#include "conv1d_1.c"
#include "weights/conv1d_1.c" // InputLayer is excluded
#include "max_pooling1d.c" // InputLayer is excluded
#include "conv_shortcut.c"
#include "weights/conv_shortcut.c" // InputLayer is excluded
#include "conv_ref.c"
#include "weights/conv_ref.c" // InputLayer is excluded
#include "max_pooling1d_1.c" // InputLayer is excluded
#include "add.c" // InputLayer is excluded
#include "conv1d_2.c"
#include "weights/conv1d_2.c" // InputLayer is excluded
#include "conv_ref_1.c"
#include "weights/conv_ref_1.c" // InputLayer is excluded
#include "add_1.c" // InputLayer is excluded
#include "max_pooling1d_2.c" // InputLayer is excluded
#include "flatten.c" // InputLayer is excluded
#include "dense.c"
#include "weights/dense.c"
#endif


void cnn(
  const input_t input,
  dense_output_type dense_output) {
  
  // Output array allocation
  static union {
    conv1d_output_type conv1d_output;
    conv_ref_output_type conv_ref_output;
    conv1d_2_output_type conv1d_2_output;
    add_1_output_type add_1_output;
  } activations1;

  static union {
    conv1d_1_output_type conv1d_1_output;
    conv_shortcut_output_type conv_shortcut_output;
    add_output_type add_output;
    max_pooling1d_2_output_type max_pooling1d_2_output;
    flatten_output_type flatten_output;
  } activations2;

  static union {
    max_pooling1d_output_type max_pooling1d_output;
    max_pooling1d_1_output_type max_pooling1d_1_output;
    conv_ref_1_output_type conv_ref_1_output;
  } activations3;


// Model layers call chain 
  
  
  conv1d( // First layer uses input passed as model parameter
    input,
    conv1d_kernel,
    conv1d_bias,
    activations1.conv1d_output
    );
  
  
  conv1d_1(
    activations1.conv1d_output,
    conv1d_1_kernel,
    conv1d_1_bias,
    activations2.conv1d_1_output
    );
  
  
  max_pooling1d(
    activations2.conv1d_1_output,
    activations3.max_pooling1d_output
    );
  
  
  conv_shortcut(
    activations1.conv1d_output,
    conv_shortcut_kernel,
    conv_shortcut_bias,
    activations2.conv_shortcut_output
    );
  
  
  conv_ref(
    activations3.max_pooling1d_output,
    conv_ref_kernel,
    conv_ref_bias,
    activations1.conv_ref_output
    );
  
  
  max_pooling1d_1(
    activations2.conv_shortcut_output,
    activations3.max_pooling1d_1_output
    );
  
  
  add(
    activations1.conv_ref_output,
    activations3.max_pooling1d_1_output,
    activations2.add_output
    );
  
  
  conv1d_2(
    activations2.add_output,
    conv1d_2_kernel,
    conv1d_2_bias,
    activations1.conv1d_2_output
    );
  
  
  conv_ref_1(
    activations1.conv1d_2_output,
    conv_ref_1_kernel,
    conv_ref_1_bias,
    activations3.conv_ref_1_output
    );
  
  
  add_1(
    activations3.conv_ref_1_output,
    activations2.add_output,
    activations1.add_1_output
    );
  
  
  max_pooling1d_2(
    activations1.add_1_output,
    activations2.max_pooling1d_2_output
    );
  
  
  flatten(
    activations2.max_pooling1d_2_output,
    activations2.flatten_output
    );
  
  
  dense(
    activations2.flatten_output,
    dense_kernel,
    dense_bias,// Last layer uses output passed as model parameter
    dense_output
    );
}

#ifdef __cplusplus
} // extern "C"
#endif
