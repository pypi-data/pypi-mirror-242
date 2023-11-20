// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: xla/service/cpu/executable.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fexecutable_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fexecutable_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "xla/service/cpu/xla_framework.pb.h"
#include "xla/service/hlo.pb.h"
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_xla_2fservice_2fcpu_2fexecutable_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_xla_2fservice_2fcpu_2fexecutable_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_xla_2fservice_2fcpu_2fexecutable_2eproto;
namespace xla {
namespace cpu {
class XlaRuntimeCpuExecutableProto;
struct XlaRuntimeCpuExecutableProtoDefaultTypeInternal;
extern XlaRuntimeCpuExecutableProtoDefaultTypeInternal _XlaRuntimeCpuExecutableProto_default_instance_;
}  // namespace cpu
}  // namespace xla
PROTOBUF_NAMESPACE_OPEN
template<> ::xla::cpu::XlaRuntimeCpuExecutableProto* Arena::CreateMaybeMessage<::xla::cpu::XlaRuntimeCpuExecutableProto>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace xla {
namespace cpu {

// ===================================================================

class XlaRuntimeCpuExecutableProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:xla.cpu.XlaRuntimeCpuExecutableProto) */ {
 public:
  inline XlaRuntimeCpuExecutableProto() : XlaRuntimeCpuExecutableProto(nullptr) {}
  ~XlaRuntimeCpuExecutableProto() override;
  explicit PROTOBUF_CONSTEXPR XlaRuntimeCpuExecutableProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  XlaRuntimeCpuExecutableProto(const XlaRuntimeCpuExecutableProto& from);
  XlaRuntimeCpuExecutableProto(XlaRuntimeCpuExecutableProto&& from) noexcept
    : XlaRuntimeCpuExecutableProto() {
    *this = ::std::move(from);
  }

  inline XlaRuntimeCpuExecutableProto& operator=(const XlaRuntimeCpuExecutableProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline XlaRuntimeCpuExecutableProto& operator=(XlaRuntimeCpuExecutableProto&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  inline const ::PROTOBUF_NAMESPACE_ID::UnknownFieldSet& unknown_fields() const {
    return _internal_metadata_.unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>(::PROTOBUF_NAMESPACE_ID::UnknownFieldSet::default_instance);
  }
  inline ::PROTOBUF_NAMESPACE_ID::UnknownFieldSet* mutable_unknown_fields() {
    return _internal_metadata_.mutable_unknown_fields<::PROTOBUF_NAMESPACE_ID::UnknownFieldSet>();
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const XlaRuntimeCpuExecutableProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const XlaRuntimeCpuExecutableProto* internal_default_instance() {
    return reinterpret_cast<const XlaRuntimeCpuExecutableProto*>(
               &_XlaRuntimeCpuExecutableProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(XlaRuntimeCpuExecutableProto& a, XlaRuntimeCpuExecutableProto& b) {
    a.Swap(&b);
  }
  inline void Swap(XlaRuntimeCpuExecutableProto* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(XlaRuntimeCpuExecutableProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  XlaRuntimeCpuExecutableProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<XlaRuntimeCpuExecutableProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const XlaRuntimeCpuExecutableProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const XlaRuntimeCpuExecutableProto& from) {
    XlaRuntimeCpuExecutableProto::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(XlaRuntimeCpuExecutableProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "xla.cpu.XlaRuntimeCpuExecutableProto";
  }
  protected:
  explicit XlaRuntimeCpuExecutableProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kXlaRuntimeExecutableFieldNumber = 1,
    kXlaFrameworkMappingFieldNumber = 2,
  };
  // optional .xla.XlaRuntimeExecutableProto xla_runtime_executable = 1;
  bool has_xla_runtime_executable() const;
  private:
  bool _internal_has_xla_runtime_executable() const;
  public:
  void clear_xla_runtime_executable();
  const ::xla::XlaRuntimeExecutableProto& xla_runtime_executable() const;
  PROTOBUF_NODISCARD ::xla::XlaRuntimeExecutableProto* release_xla_runtime_executable();
  ::xla::XlaRuntimeExecutableProto* mutable_xla_runtime_executable();
  void set_allocated_xla_runtime_executable(::xla::XlaRuntimeExecutableProto* xla_runtime_executable);
  private:
  const ::xla::XlaRuntimeExecutableProto& _internal_xla_runtime_executable() const;
  ::xla::XlaRuntimeExecutableProto* _internal_mutable_xla_runtime_executable();
  public:
  void unsafe_arena_set_allocated_xla_runtime_executable(
      ::xla::XlaRuntimeExecutableProto* xla_runtime_executable);
  ::xla::XlaRuntimeExecutableProto* unsafe_arena_release_xla_runtime_executable();

  // optional .xla.cpu.XlaFrameworkMappingProto xla_framework_mapping = 2;
  bool has_xla_framework_mapping() const;
  private:
  bool _internal_has_xla_framework_mapping() const;
  public:
  void clear_xla_framework_mapping();
  const ::xla::cpu::XlaFrameworkMappingProto& xla_framework_mapping() const;
  PROTOBUF_NODISCARD ::xla::cpu::XlaFrameworkMappingProto* release_xla_framework_mapping();
  ::xla::cpu::XlaFrameworkMappingProto* mutable_xla_framework_mapping();
  void set_allocated_xla_framework_mapping(::xla::cpu::XlaFrameworkMappingProto* xla_framework_mapping);
  private:
  const ::xla::cpu::XlaFrameworkMappingProto& _internal_xla_framework_mapping() const;
  ::xla::cpu::XlaFrameworkMappingProto* _internal_mutable_xla_framework_mapping();
  public:
  void unsafe_arena_set_allocated_xla_framework_mapping(
      ::xla::cpu::XlaFrameworkMappingProto* xla_framework_mapping);
  ::xla::cpu::XlaFrameworkMappingProto* unsafe_arena_release_xla_framework_mapping();

  // @@protoc_insertion_point(class_scope:xla.cpu.XlaRuntimeCpuExecutableProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::HasBits<1> _has_bits_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
    ::xla::XlaRuntimeExecutableProto* xla_runtime_executable_;
    ::xla::cpu::XlaFrameworkMappingProto* xla_framework_mapping_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_xla_2fservice_2fcpu_2fexecutable_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// XlaRuntimeCpuExecutableProto

// optional .xla.XlaRuntimeExecutableProto xla_runtime_executable = 1;
inline bool XlaRuntimeCpuExecutableProto::_internal_has_xla_runtime_executable() const {
  bool value = (_impl_._has_bits_[0] & 0x00000001u) != 0;
  PROTOBUF_ASSUME(!value || _impl_.xla_runtime_executable_ != nullptr);
  return value;
}
inline bool XlaRuntimeCpuExecutableProto::has_xla_runtime_executable() const {
  return _internal_has_xla_runtime_executable();
}
inline const ::xla::XlaRuntimeExecutableProto& XlaRuntimeCpuExecutableProto::_internal_xla_runtime_executable() const {
  const ::xla::XlaRuntimeExecutableProto* p = _impl_.xla_runtime_executable_;
  return p != nullptr ? *p : reinterpret_cast<const ::xla::XlaRuntimeExecutableProto&>(
      ::xla::_XlaRuntimeExecutableProto_default_instance_);
}
inline const ::xla::XlaRuntimeExecutableProto& XlaRuntimeCpuExecutableProto::xla_runtime_executable() const {
  // @@protoc_insertion_point(field_get:xla.cpu.XlaRuntimeCpuExecutableProto.xla_runtime_executable)
  return _internal_xla_runtime_executable();
}
inline void XlaRuntimeCpuExecutableProto::unsafe_arena_set_allocated_xla_runtime_executable(
    ::xla::XlaRuntimeExecutableProto* xla_runtime_executable) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.xla_runtime_executable_);
  }
  _impl_.xla_runtime_executable_ = xla_runtime_executable;
  if (xla_runtime_executable) {
    _impl_._has_bits_[0] |= 0x00000001u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000001u;
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:xla.cpu.XlaRuntimeCpuExecutableProto.xla_runtime_executable)
}
inline ::xla::XlaRuntimeExecutableProto* XlaRuntimeCpuExecutableProto::release_xla_runtime_executable() {
  _impl_._has_bits_[0] &= ~0x00000001u;
  ::xla::XlaRuntimeExecutableProto* temp = _impl_.xla_runtime_executable_;
  _impl_.xla_runtime_executable_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::xla::XlaRuntimeExecutableProto* XlaRuntimeCpuExecutableProto::unsafe_arena_release_xla_runtime_executable() {
  // @@protoc_insertion_point(field_release:xla.cpu.XlaRuntimeCpuExecutableProto.xla_runtime_executable)
  _impl_._has_bits_[0] &= ~0x00000001u;
  ::xla::XlaRuntimeExecutableProto* temp = _impl_.xla_runtime_executable_;
  _impl_.xla_runtime_executable_ = nullptr;
  return temp;
}
inline ::xla::XlaRuntimeExecutableProto* XlaRuntimeCpuExecutableProto::_internal_mutable_xla_runtime_executable() {
  _impl_._has_bits_[0] |= 0x00000001u;
  if (_impl_.xla_runtime_executable_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::XlaRuntimeExecutableProto>(GetArenaForAllocation());
    _impl_.xla_runtime_executable_ = p;
  }
  return _impl_.xla_runtime_executable_;
}
inline ::xla::XlaRuntimeExecutableProto* XlaRuntimeCpuExecutableProto::mutable_xla_runtime_executable() {
  ::xla::XlaRuntimeExecutableProto* _msg = _internal_mutable_xla_runtime_executable();
  // @@protoc_insertion_point(field_mutable:xla.cpu.XlaRuntimeCpuExecutableProto.xla_runtime_executable)
  return _msg;
}
inline void XlaRuntimeCpuExecutableProto::set_allocated_xla_runtime_executable(::xla::XlaRuntimeExecutableProto* xla_runtime_executable) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.xla_runtime_executable_);
  }
  if (xla_runtime_executable) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(xla_runtime_executable));
    if (message_arena != submessage_arena) {
      xla_runtime_executable = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, xla_runtime_executable, submessage_arena);
    }
    _impl_._has_bits_[0] |= 0x00000001u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000001u;
  }
  _impl_.xla_runtime_executable_ = xla_runtime_executable;
  // @@protoc_insertion_point(field_set_allocated:xla.cpu.XlaRuntimeCpuExecutableProto.xla_runtime_executable)
}

// optional .xla.cpu.XlaFrameworkMappingProto xla_framework_mapping = 2;
inline bool XlaRuntimeCpuExecutableProto::_internal_has_xla_framework_mapping() const {
  bool value = (_impl_._has_bits_[0] & 0x00000002u) != 0;
  PROTOBUF_ASSUME(!value || _impl_.xla_framework_mapping_ != nullptr);
  return value;
}
inline bool XlaRuntimeCpuExecutableProto::has_xla_framework_mapping() const {
  return _internal_has_xla_framework_mapping();
}
inline const ::xla::cpu::XlaFrameworkMappingProto& XlaRuntimeCpuExecutableProto::_internal_xla_framework_mapping() const {
  const ::xla::cpu::XlaFrameworkMappingProto* p = _impl_.xla_framework_mapping_;
  return p != nullptr ? *p : reinterpret_cast<const ::xla::cpu::XlaFrameworkMappingProto&>(
      ::xla::cpu::_XlaFrameworkMappingProto_default_instance_);
}
inline const ::xla::cpu::XlaFrameworkMappingProto& XlaRuntimeCpuExecutableProto::xla_framework_mapping() const {
  // @@protoc_insertion_point(field_get:xla.cpu.XlaRuntimeCpuExecutableProto.xla_framework_mapping)
  return _internal_xla_framework_mapping();
}
inline void XlaRuntimeCpuExecutableProto::unsafe_arena_set_allocated_xla_framework_mapping(
    ::xla::cpu::XlaFrameworkMappingProto* xla_framework_mapping) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.xla_framework_mapping_);
  }
  _impl_.xla_framework_mapping_ = xla_framework_mapping;
  if (xla_framework_mapping) {
    _impl_._has_bits_[0] |= 0x00000002u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000002u;
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:xla.cpu.XlaRuntimeCpuExecutableProto.xla_framework_mapping)
}
inline ::xla::cpu::XlaFrameworkMappingProto* XlaRuntimeCpuExecutableProto::release_xla_framework_mapping() {
  _impl_._has_bits_[0] &= ~0x00000002u;
  ::xla::cpu::XlaFrameworkMappingProto* temp = _impl_.xla_framework_mapping_;
  _impl_.xla_framework_mapping_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::xla::cpu::XlaFrameworkMappingProto* XlaRuntimeCpuExecutableProto::unsafe_arena_release_xla_framework_mapping() {
  // @@protoc_insertion_point(field_release:xla.cpu.XlaRuntimeCpuExecutableProto.xla_framework_mapping)
  _impl_._has_bits_[0] &= ~0x00000002u;
  ::xla::cpu::XlaFrameworkMappingProto* temp = _impl_.xla_framework_mapping_;
  _impl_.xla_framework_mapping_ = nullptr;
  return temp;
}
inline ::xla::cpu::XlaFrameworkMappingProto* XlaRuntimeCpuExecutableProto::_internal_mutable_xla_framework_mapping() {
  _impl_._has_bits_[0] |= 0x00000002u;
  if (_impl_.xla_framework_mapping_ == nullptr) {
    auto* p = CreateMaybeMessage<::xla::cpu::XlaFrameworkMappingProto>(GetArenaForAllocation());
    _impl_.xla_framework_mapping_ = p;
  }
  return _impl_.xla_framework_mapping_;
}
inline ::xla::cpu::XlaFrameworkMappingProto* XlaRuntimeCpuExecutableProto::mutable_xla_framework_mapping() {
  ::xla::cpu::XlaFrameworkMappingProto* _msg = _internal_mutable_xla_framework_mapping();
  // @@protoc_insertion_point(field_mutable:xla.cpu.XlaRuntimeCpuExecutableProto.xla_framework_mapping)
  return _msg;
}
inline void XlaRuntimeCpuExecutableProto::set_allocated_xla_framework_mapping(::xla::cpu::XlaFrameworkMappingProto* xla_framework_mapping) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.xla_framework_mapping_);
  }
  if (xla_framework_mapping) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(xla_framework_mapping));
    if (message_arena != submessage_arena) {
      xla_framework_mapping = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, xla_framework_mapping, submessage_arena);
    }
    _impl_._has_bits_[0] |= 0x00000002u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000002u;
  }
  _impl_.xla_framework_mapping_ = xla_framework_mapping;
  // @@protoc_insertion_point(field_set_allocated:xla.cpu.XlaRuntimeCpuExecutableProto.xla_framework_mapping)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__

// @@protoc_insertion_point(namespace_scope)

}  // namespace cpu
}  // namespace xla

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_xla_2fservice_2fcpu_2fexecutable_2eproto
