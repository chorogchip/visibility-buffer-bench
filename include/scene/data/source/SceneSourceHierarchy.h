#pragma once

#include <cstdint>
#include <string>
#include <vector>

#include <DirectXMath.h>

#include "math/AABB.h"
#include "scene/data/source/SceneConstants.h"
#include "scene/data/source/SceneSourceSemantic.h"

namespace scene::source {

    // Compact TRS is the default representation. The optional affine matrix
    // preserves composed transforms (including shear) that cannot be lowered
    // losslessly to TRS. source_index remains reversible for source arrays.
    struct InstanceTransform {
        DirectX::XMFLOAT3 translation = { 0.0f, 0.0f, 0.0f };
        DirectX::XMFLOAT4 rotation = { 0.0f, 0.0f, 0.0f, 1.0f };
        DirectX::XMFLOAT3 scale = { 1.0f, 1.0f, 1.0f };
        uint32_t source_index = SceneConstants::INVALID_INDEX;
        DirectX::XMFLOAT4X4 matrix = {
            1.0f, 0.0f, 0.0f, 0.0f,
            0.0f, 1.0f, 0.0f, 0.0f,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };
        bool has_matrix = false;
    };

    static_assert(sizeof(InstanceTransform) == 112);

    // Matrices use DirectX row-vector order and are not transposed for shaders.
    // An instance range belongs to this node and uses node-local transforms.
    struct Node {
        std::string name;
        std::vector<uint32_t> children;
        DirectX::XMFLOAT4X4 local_transform = {
            1.0f, 0.0f, 0.0f, 0.0f,
            0.0f, 1.0f, 0.0f, 0.0f,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };
        uint32_t mesh_id = SceneConstants::INVALID_INDEX;
        uint32_t polygon_mesh_id = SceneConstants::INVALID_INDEX;
        uint32_t camera_id = SceneConstants::INVALID_INDEX;
        uint32_t first_instance = 0;
        uint32_t instance_count = 0;

        math::AABB world_bounds{};
        std::string stable_id;

        SourceReference source;
        uint32_t parent_node_id = SceneConstants::INVALID_INDEX;
        DirectX::XMFLOAT4X4 world_transform = {
            1.0f, 0.0f, 0.0f, 0.0f,
            0.0f, 1.0f, 0.0f, 0.0f,
            0.0f, 0.0f, 1.0f, 0.0f,
            0.0f, 0.0f, 0.0f, 1.0f
        };
        std::string prim_type;
        std::vector<std::string> applied_schemas;
        std::string purpose;
        bool visible = true;
        bool active = true;
        bool loaded = true;
        bool defined = true;
        bool abstract = false;
        bool reset_xform_stack = false;
        bool native_instance = false;

    };
}
