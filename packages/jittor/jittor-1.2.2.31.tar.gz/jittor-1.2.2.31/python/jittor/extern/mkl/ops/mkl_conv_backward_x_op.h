// ***************************************************************
// Copyright (c) 2021 Jittor. All Rights Reserved. 
// Maintainers: 
//     Guowei Yang <471184555@qq.com>
//     Dun Liang <randonlang@gmail.com>. 
// 
// This file is subject to the terms and conditions defined in
// file 'LICENSE.txt', which is part of this source code package.
// ***************************************************************
#pragma once
#include "op.h"

namespace jittor {

struct MklConvBackwardXOp : Op {
    Var* w, * dy, * dx;
    int xh, xw, stride, padding, dilation, groups;
    string xformat, wformat, yformat;

    MklConvBackwardXOp(Var* w, Var* y, int height, int width, int stride, int padding, int dilation, int groups=1, string xformat="abcd", string wformat="oihw", string yformat="abcd");
    
    const char* name() const override { return "mkl_conv_backward_x"; }
    void infer_shape() override;
    DECLARE_jit_run;
};

} // jittor