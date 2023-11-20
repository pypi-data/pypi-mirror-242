/* Copyright 2018 The TensorFlow Authors. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_LAYOUT_H_
#define XLA_LAYOUT_H_

#include <cstdint>
#include <limits>
#include <memory>
#include <ostream>
#include <string>

#include "absl/container/inlined_vector.h"
#include "absl/types/span.h"
#include "xla/printer.h"
#include "xla/util.h"
#include "xla/xla_data.pb.h"
#include "tsl/platform/logging.h"  // IWYU pragma: keep

namespace xla {

class Shape;

// Describes a tile used in tiling-based layout. Refer to
// g3doc/third_party/tensorflow/compiler/xla/g3doc/tiled_layout.md for
// details.
class Tile {
 public:
  Tile() = default;
  explicit Tile(absl::Span<const int64_t> dimensions)
      : dimensions_(dimensions.begin(), dimensions.end()) {}

  // De/Serialize a Tile to and from a TileProto.
  static Tile CreateFromProto(const TileProto& tile_proto) {
    return Tile(tile_proto.dimensions());
  }
  TileProto ToProto() const;

  bool operator==(const Tile& other) const {
    return dimensions() == other.dimensions();
  }
  bool operator!=(const Tile& other) const { return !(*this == other); }

  void Print(Printer* printer) const;

  std::string ToString() const;

  // Returns the bound of the tile in the given dimension index.
  int64_t dimension(int i) const { return dimensions_.at(i); }

  // Returns the dimensions of the tile.
  absl::Span<const int64_t> dimensions() const { return dimensions_; }

  Tile& add_dimensions(int64_t value) {
    dimensions_.push_back(value);
    return *this;
  }

  Tile& clear_dimensions() {
    dimensions_.clear();
    return *this;
  }

  // This dimension size means the corresponding dimension in the shape is
  // combined with the next minor dimension before tiling is applied.
  static constexpr int64_t kCombineDimension =
      std::numeric_limits<int64_t>::min();

  template <typename H>
  friend H AbslHashValue(H h, const Tile& t) {
    return H::combine(std::move(h), t.dimensions_);
  }

 private:
  // The bounds of the tile.
  absl::InlinedVector<int64_t, 2> dimensions_;
};

using TileVector = absl::InlinedVector<Tile, 3>;

// TODO: Rename the `dim_level_types` field to `lvl_types`, so that it
// matches `mlir::sparse_tensor::SparseTensorEncodingAttr`.
class Layout {
 public:
  Layout();
  Layout(const Layout& other);
  Layout(Layout&& other);
  ~Layout();

  // Constructs a dense layout with the given minor-to-major order.
  explicit Layout(absl::Span<const int64_t> minor_to_major);

  // Constructs a dense tiled layout with the given minor-to-major order, dim
  // level types, and tiles.
  explicit Layout(absl::Span<const int64_t> minor_to_major,
                  absl::Span<const DimLevelType> dim_level_types,
                  absl::Span<const bool> dim_unique,
                  absl::Span<const bool> dim_ordered,
                  absl::Span<const Tile> tiles,
                  PrimitiveType index_primitive_type = PRIMITIVE_TYPE_INVALID,
                  PrimitiveType element_primitive_type = PRIMITIVE_TYPE_INVALID,
                  int64_t element_size_in_bits = 0, int64_t memory_space = 0,
                  std::unique_ptr<Shape> physical_shape = nullptr,
                  int64_t dynamic_shape_metadata_prefix_bytes = 0);

  Layout& operator=(const Layout& other);
  Layout& operator=(Layout&& other);

  // Construct a shape from a LayoutProto.
  static Layout CreateFromProto(const LayoutProto& proto);

  // Returns a LayoutProto representation of the Layout.
  LayoutProto ToProto() const;

  // Prints a human-readable string that represents this layout.
  void Print(Printer* printer) const;

  // Returns a human-readable string that represents this layout.
  std::string ToString() const;

  // Equal is a configurable functor to check the equality of two layouts.
  //
  // Examples:
  //
  // - Comparing two layouts ignoring their difference in tiles:
  //   Equal().IgnoreTiles()(layout1, layout2);
  class Equal {
   public:
    Equal() = default;

    bool operator()(const Layout& lhs, const Layout& rhs);

    Equal& IgnoreTiles() {
      ignore_tiles_ = true;
      return *this;
    }

    Equal& IgnoreIndexPrimitiveType() {
      ignore_index_primitive_type_ = true;
      return *this;
    }

    Equal& IgnorePointerPrimitiveType() {
      ignore_pointer_primitive_type_ = true;
      return *this;
    }

    Equal& IgnoreMemorySpace() {
      ignore_memory_space_ = true;
      return *this;
    }

    Equal& IgnorePhysicalShape() {
      ignore_physical_shape_ = true;
      return *this;
    }

    Equal& IgnoreElementSize() {
      ignore_element_size_ = true;
      return *this;
    }

    Equal& MinorToMajorOnly() {
      return IgnoreTiles()
          .IgnoreIndexPrimitiveType()
          .IgnorePointerPrimitiveType()
          .IgnoreMemorySpace()
          .IgnorePhysicalShape()
          .IgnoreElementSize();
    }

   private:
    bool ignore_tiles_ = false;
    bool ignore_element_size_ = false;
    bool ignore_index_primitive_type_ = false;
    bool ignore_pointer_primitive_type_ = false;
    bool ignore_memory_space_ = false;
    bool ignore_physical_shape_ = false;
  };

  bool operator==(const Layout& other) const;
  bool operator!=(const Layout& other) const { return !(*this == other); }

  // The following methods mirror the protobuf generated code interface for the
  // message LayoutProto. This enabled easy migration of this data structure
  // from a proto to a proper C++ class.
  //
  // TODO(b/29771030): Replace or augment these methods with a more ergonomic
  // interface.

  // Methods for accessing the DimLevelType array.
  int dim_level_types_size() const { return dim_level_types_.size(); }
  DimLevelType dim_level_type(int index) const {
    return dim_level_types_.at(index);
  }
  Layout& set_dim_level_type(int index, DimLevelType dim_level_type) {
    dim_level_types_.at(index) = dim_level_type;
    return *this;
  }
  Layout& add_dim_level_type(DimLevelType dim_level_type) {
    dim_level_types_.push_back(dim_level_type);
    return *this;
  }
  Layout& clear_dim_level_types() {
    dim_level_types_.clear();
    return *this;
  }
  absl::Span<const DimLevelType> dim_level_types() const {
    return dim_level_types_;
  }
  DimLevelTypeVector* mutable_dim_level_types() { return &dim_level_types_; }

  // Methods for accessing the dim_unique array.
  int dim_unique_size() const { return dim_unique_.size(); }
  bool dim_unique(int index) const { return dim_unique_.at(index); }
  Layout& set_dim_unique(int index, bool unique) {
    dim_unique_.at(index) = unique;
    return *this;
  }
  Layout& add_dim_unique(bool unique) {
    dim_unique_.push_back(unique);
    return *this;
  }
  Layout& clear_dim_unique() {
    dim_unique_.clear();
    return *this;
  }
  absl::Span<const bool> dim_unique() const { return dim_unique_; }
  absl::InlinedVector<bool, InlineRank()>* mutable_dim_unique() {
    return &dim_unique_;
  }

  // Methods for accessing the dim_ordered array.
  int dim_ordered_size() const { return dim_ordered_.size(); }
  bool dim_ordered(int index) const { return dim_ordered_.at(index); }
  Layout& set_dim_ordered(int index, bool ordered) {
    dim_ordered_.at(index) = ordered;
    return *this;
  }
  Layout& add_dim_ordered(bool ordered) {
    dim_ordered_.push_back(ordered);
    return *this;
  }
  Layout& clear_dim_ordered() {
    dim_ordered_.clear();
    return *this;
  }
  absl::Span<const bool> dim_ordered() const { return dim_ordered_; }
  absl::InlinedVector<bool, InlineRank()>* mutable_dim_ordered() {
    return &dim_ordered_;
  }

  // Methods for accessing the minor-to-major array.
  int minor_to_major_size() const { return minor_to_major_.size(); }
  int64_t minor_to_major(int index) const { return minor_to_major_.at(index); }
  Layout& set_minor_to_major(int index, int64_t value) {
    minor_to_major_.at(index) = value;
    return *this;
  }
  Layout& add_minor_to_major(int64_t value) {
    minor_to_major_.push_back(value);
    return *this;
  }
  Layout& clear_minor_to_major() {
    minor_to_major_.clear();
    return *this;
  }
  // Removes the given dimension from 'minor_to_major_', and adjusts the other
  // dimensions accordingly. Also adjusts 'dim_level_types_', 'dim_ordered_' and
  // 'dim_unique_' in case it is a sparse layout.
  Layout& DeleteDimension(int64_t dim_to_delete);
  absl::Span<const int64_t> minor_to_major() const { return minor_to_major_; }
  DimensionVector* mutable_minor_to_major() { return &minor_to_major_; }

  // Methods for accessing the tile field.
  int64_t tiles_size() const { return tiles_.size(); }
  const Tile& tiles(int index) const { return tiles_.at(index); }
  Tile* mutable_tiles(int index) { return &tiles_.at(index); }
  Tile* add_tiles() {
    tiles_.push_back(Tile());
    return &tiles_.back();
  }
  Layout& clear_tiles() {
    tiles_.clear();
    return *this;
  }
  absl::Span<const Tile> tiles() const { return tiles_; }
  TileVector* mutable_tiles() { return &tiles_; }

  int64_t element_size_in_bits() const { return element_size_in_bits_; }
  Layout& set_element_size_in_bits(int64_t value) {
    element_size_in_bits_ = value;
    return *this;
  }

  PrimitiveType index_primitive_type() const { return index_primitive_type_; }
  Layout& set_index_primitive_type(PrimitiveType value) {
    index_primitive_type_ = value;
    return *this;
  }

  PrimitiveType pointer_primitive_type() const {
    return pointer_primitive_type_;
  }
  Layout& set_pointer_primitive_type(PrimitiveType value) {
    pointer_primitive_type_ = value;
    return *this;
  }

  static constexpr int64_t kDefaultMemorySpace = 0;
  static constexpr int64_t kGenericFastMemorySpace = 1;
  int64_t memory_space() const { return memory_space_; }
  Layout& set_memory_space(int64_t value) {
    memory_space_ = value;
    return *this;
  }

  // Methods for accessing the physical shape.
  bool has_physical_shape() const { return physical_shape_ != nullptr; }
  const Shape& physical_shape() const {
    CHECK(has_physical_shape());
    return *physical_shape_;
  }
  Shape* mutable_physical_shape();
  void clear_physical_shape();

  int64_t dynamic_shape_metadata_prefix_bytes() const {
    return dynamic_shape_metadata_prefix_bytes_;
  }
  void set_dynamic_shape_metadata_prefix_bytes(int64_t bytes) {
    dynamic_shape_metadata_prefix_bytes_ = bytes;
  }

  void Swap(Layout* other) {
    using std::swap;
    swap(*this, *other);
  }

  void Clear() { *this = Layout(); }

  template <typename H>
  friend H AbslHashValue(H h, const Layout& l) {
    return H::combine(std::move(h), l.minor_to_major_, l.tiles_,
                      l.element_size_in_bits_, l.index_primitive_type_,
                      l.pointer_primitive_type_, l.memory_space_);
  }

 private:
  // The list of dimension level types, indicating the method that will be used
  // to represent each dimension of the array.
  DimLevelTypeVector dim_level_types_;

  // Whether each DimLevelType is unique and ordered.
  absl::InlinedVector<bool, InlineRank()> dim_unique_;
  absl::InlinedVector<bool, InlineRank()> dim_ordered_;

  // A map from physical dimension numbers to logical dimension numbers.
  // The first element is the most minor physical dimension (fastest varying
  // index) and the last the most major (slowest varying index). The contents of
  // the vector are the indices of the *logical* dimensions in the shape.
  //
  // For example, in shape f32[8,100,100,3]{3,0,2,1}, the logical dimensions
  // are [8,100,100,3] and minor_to_major_ is {3,0,2,1}.
  // So, the most minor physical dimension is [8,100,100,3][3], which is size 3.
  // The second most minor is [8,100,100,3][0], which is size 8.
  // The third most minor is [8,100,100,3][2], which is size 100.
  // And the major dim is [8,100,100,3][1], which is size 100.
  DimensionVector minor_to_major_;

  // The tiles used in tiling-based layout.
  TileVector tiles_;

  // The primitive type to use for sparse array indices and pointers.  Each of
  // these must either be INVALID, or an unsigned integer type.
  PrimitiveType index_primitive_type_ = PRIMITIVE_TYPE_INVALID;
  PrimitiveType pointer_primitive_type_ = PRIMITIVE_TYPE_INVALID;

  // The number of bits used to store an individual array element.
  // When the value is 0, default to ShapeUtil::ByteSizeOfPrimitiveType.
  int64_t element_size_in_bits_ = 0;

  // The assigned memory space.
  int64_t memory_space_ = 0;

  // The physical on-device shape used to represent a sparse array.
  std::unique_ptr<Shape> physical_shape_;

  // The dynamic shape metadata size in bytes in front of the shape data. The
  // field may be non-zero for a static shape whose associated buffer is for a
  // dynamic shape, e.g. a result of SliceToDynamic.
  int64_t dynamic_shape_metadata_prefix_bytes_ = 0;
};

std::ostream& operator<<(std::ostream& out, const Tile& Tile);
std::ostream& operator<<(std::ostream& out, const Layout& layout);

}  // namespace xla

#endif  // XLA_LAYOUT_H_
