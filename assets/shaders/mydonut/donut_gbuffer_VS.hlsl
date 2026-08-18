/*
* Copyright (c) 2014-2024, NVIDIA CORPORATION. All rights reserved.
*
* Permission is hereby granted, free of charge, to any person obtaining a
* copy of this software and associated documentation files (the "Software"),
* to deal in the Software without restriction, including without limitation
* the rights to use, copy, modify, merge, publish, distribute, sublicense,
* and/or sell copies of the Software, and to permit persons to whom the
* Software is furnished to do so, subject to the following conditions:
*
* The above copyright notice and this permission notice shall be included in
* all copies or substantial portions of the Software.
*
* THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
* IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
* FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
* THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
* LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
* FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
* DEALINGS IN THE SOFTWARE.
*/

#include "..\common\mydonut_scene_abi.hlsli"

StructuredBuffer<InstanceData> t_Instances :
    register(t10, space1);
ByteAddressBuffer t_Vertices :
    register(t11, space1);
StructuredBuffer<DrawInstanceData> t_DrawInstances :
    register(t12, space1);
StructuredBuffer<uint> t_DrawInstanceIDs :
    register(t13, space1);

cbuffer c_Push : register(b1, space1)
{
    GBufferPushConstants g_Push;
};

cbuffer c_GBuffer : register(b2, space2)
{
    GBufferFillConstants g_GBuffer;
};

struct VSOutput
{
    float4 clipPosition : SV_Position;
    float2 texCoord : TEXCOORD0;
    float3 normal : NORMAL0;
    float4 tangent : TANGENT0;
};

VSOutput main(uint vertexId : SV_VertexID, uint instanceId : SV_InstanceID)
{
    const uint compactedSlot = instanceId + g_Push.startInstanceLocation;
    const uint drawInstanceID = t_DrawInstanceIDs[compactedSlot];
    const DrawInstanceData drawInstance = t_DrawInstances[drawInstanceID];
    const InstanceData instance = t_Instances[drawInstance.instanceID];
    const uint vertexIndex = vertexId + g_Push.startVertexLocation;

    const float3 position = asfloat(t_Vertices.Load3(
        g_Push.positionOffset + vertexIndex * SizeOfPosition));
    const float2 texCoord = asfloat(t_Vertices.Load2(
        g_Push.texCoordOffset + vertexIndex * SizeOfTexcoord));
    const uint packedNormal = t_Vertices.Load(
        g_Push.normalOffset + vertexIndex * SizeOfPackedNormal);
    const uint packedTangent = t_Vertices.Load(
        g_Push.tangentOffset + vertexIndex * SizeOfPackedNormal);

    const float3 worldPosition = TransformPoint(instance.transform, position);
    const float3 worldNormal = TransformVector(
        instance.transform, UnpackRgb8Snorm(packedNormal));
    const float4 tangent = UnpackRgba8Snorm(packedTangent);
    const float3 worldTangent = TransformVector(instance.transform, tangent.xyz);

    VSOutput output;
    output.clipPosition = mul(float4(worldPosition, 1.0), g_GBuffer.view.matWorldToClip);
    output.texCoord = texCoord;
    output.normal = worldNormal;
    output.tangent = float4(worldTangent, tangent.w);
    return output;
}
