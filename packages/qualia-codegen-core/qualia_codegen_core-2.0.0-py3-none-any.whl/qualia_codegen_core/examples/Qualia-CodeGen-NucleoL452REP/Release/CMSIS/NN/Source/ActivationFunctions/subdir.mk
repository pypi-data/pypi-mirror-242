################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/piernov/devel/qualia/qualia-codegen-core/src/qualia_codegen_core/examples/third_party/cmsis/CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.c \
/home/piernov/devel/qualia/qualia-codegen-core/src/qualia_codegen_core/examples/third_party/cmsis/CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.c 

C_DEPS += \
./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.d \
./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.d 

OBJS += \
./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.o \
./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.o 


# Each subdirectory must supply rules for building sources it contributes
CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.o: /home/piernov/devel/qualia/qualia-codegen-core/src/qualia_codegen_core/examples/third_party/cmsis/CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.c CMSIS/NN/Source/ActivationFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu17 -DUSE_HAL_DRIVER -DSTM32L452xx -c -I../Core/Inc -I../../third_party/cmsis/CMSIS/DSP/Include -I../../third_party/cmsis/CMSIS/NN/Include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -Ofast -ffunction-sections -fdata-sections -Wall -Wextra -Werror=double-promotion -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"
CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.o: /home/piernov/devel/qualia/qualia-codegen-core/src/qualia_codegen_core/examples/third_party/cmsis/CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.c CMSIS/NN/Source/ActivationFunctions/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu17 -DUSE_HAL_DRIVER -DSTM32L452xx -c -I../Core/Inc -I../../third_party/cmsis/CMSIS/DSP/Include -I../../third_party/cmsis/CMSIS/NN/Include -I../Drivers/STM32L4xx_HAL_Driver/Inc -I../Drivers/STM32L4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32L4xx/Include -I../Drivers/CMSIS/Include -Ofast -ffunction-sections -fdata-sections -Wall -Wextra -Werror=double-promotion -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-CMSIS-2f-NN-2f-Source-2f-ActivationFunctions

clean-CMSIS-2f-NN-2f-Source-2f-ActivationFunctions:
	-$(RM) ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.cyclo ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.d ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.o ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q15.su ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.cyclo ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.d ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.o ./CMSIS/NN/Source/ActivationFunctions/arm_relu_q7.su

.PHONY: clean-CMSIS-2f-NN-2f-Source-2f-ActivationFunctions

