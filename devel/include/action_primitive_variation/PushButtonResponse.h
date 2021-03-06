// Generated by gencpp from file action_primitive_variation/PushButtonResponse.msg
// DO NOT EDIT!


#ifndef ACTION_PRIMITIVE_VARIATION_MESSAGE_PUSHBUTTONRESPONSE_H
#define ACTION_PRIMITIVE_VARIATION_MESSAGE_PUSHBUTTONRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace action_primitive_variation
{
template <class ContainerAllocator>
struct PushButtonResponse_
{
  typedef PushButtonResponse_<ContainerAllocator> Type;

  PushButtonResponse_()
    : success_bool(0)  {
    }
  PushButtonResponse_(const ContainerAllocator& _alloc)
    : success_bool(0)  {
  (void)_alloc;
    }



   typedef int64_t _success_bool_type;
  _success_bool_type success_bool;




  typedef boost::shared_ptr< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> const> ConstPtr;

}; // struct PushButtonResponse_

typedef ::action_primitive_variation::PushButtonResponse_<std::allocator<void> > PushButtonResponse;

typedef boost::shared_ptr< ::action_primitive_variation::PushButtonResponse > PushButtonResponsePtr;
typedef boost::shared_ptr< ::action_primitive_variation::PushButtonResponse const> PushButtonResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace action_primitive_variation

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': True, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'action_primitive_variation': ['/home/evana/apv_ws/src/action_primitive_variation/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "6e72685e7a815ec68561aa624b91e276";
  }

  static const char* value(const ::action_primitive_variation::PushButtonResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x6e72685e7a815ec6ULL;
  static const uint64_t static_value2 = 0x8561aa624b91e276ULL;
};

template<class ContainerAllocator>
struct DataType< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "action_primitive_variation/PushButtonResponse";
  }

  static const char* value(const ::action_primitive_variation::PushButtonResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 success_bool\n\
\n\
";
  }

  static const char* value(const ::action_primitive_variation::PushButtonResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.success_bool);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct PushButtonResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::action_primitive_variation::PushButtonResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::action_primitive_variation::PushButtonResponse_<ContainerAllocator>& v)
  {
    s << indent << "success_bool: ";
    Printer<int64_t>::stream(s, indent + "  ", v.success_bool);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ACTION_PRIMITIVE_VARIATION_MESSAGE_PUSHBUTTONRESPONSE_H
