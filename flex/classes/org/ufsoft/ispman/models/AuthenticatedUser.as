/**
 * @author vampas
 */
package org.ufsoft.ispman.models {
  public class AuthenticatedUser {
    public static var ALIAS : String = 'org.ufsoft.ispman.models.AuthenticatedUser';
    public var username     : String;
    public var password     : String;
    public var loginType    : int;
    public function AuthenticatedUser(username:String, password:String, loginType:int)
    {
      this.username  = username;
      this.password  = password;
      this.loginType = loginType;
    }
  }

}


