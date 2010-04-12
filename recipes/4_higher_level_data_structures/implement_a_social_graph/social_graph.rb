REDIS = Redis.new

class User
  def self.find(*ids)
    # gets a set of User objects given IDs
  end
  
  def follow(other_user)
    REDIS.sadd("user:#{self.id}:follows", other_user.id)
    REDIS.sadd("user:#{other_user.id}:followers", self.id)
  end
  
  def followers
    User.find(*REDIS.smembers("user:#{self.id}:followers"))
  end
  
  def follows
    User.find(*REDIS.smembers("user:#{self.id}:follows"))
  end
  
  def friends
    User.find(*REDIS.sinter("user:#{self.id}:followers", "user:#{self.id}:follows"))
  end
end