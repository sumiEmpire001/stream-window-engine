#pragma once
#include <cmath>
#include <cstdint>
#include <map>
#include <stdexcept>
#include <string>
#include <utility>
namespace sumi {
struct Window { unsigned count=0; double sum=0,min=0,max=0; double mean() const {return count?sum/count:0;} };
class WindowEngine {
 std::int64_t duration_; std::size_t capacity_;
 std::map<std::pair<std::int64_t,std::string>,Window> windows_;
public:
 explicit WindowEngine(std::int64_t seconds=60,std::size_t capacity=128):duration_(seconds),capacity_(capacity) {
  if(seconds<=0||capacity==0||capacity>4096)throw std::invalid_argument("invalid configuration");
 }
 bool ingest(std::int64_t timestamp,const std::string& group,double value) {
  if(group.empty()||group.size()>32||!std::isfinite(value))return false;
  const std::int64_t q=timestamp/duration_-(timestamp<0&&timestamp%duration_!=0?1:0);
  if(q>INT64_MAX/duration_||q<INT64_MIN/duration_)return false;
  auto key=std::make_pair(q*duration_,group);
  auto it=windows_.find(key);
  if(it==windows_.end()&&windows_.size()>=capacity_)return false;
  if(it!=windows_.end()&&(it->second.count==UINT32_MAX||!std::isfinite(it->second.sum+value)))return false;
  Window &w=windows_[key];if(!w.count)w.min=w.max=value;
  else {if(value<w.min)w.min=value;if(value>w.max)w.max=value;}
  w.sum+=value;++w.count;return true;
 }
 const std::map<std::pair<std::int64_t,std::string>,Window>& windows()const{return windows_;}
 void clear(){windows_.clear();}
};
}
