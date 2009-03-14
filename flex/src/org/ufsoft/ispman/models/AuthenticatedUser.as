/**
 * @author vampas
 */
package org.ufsoft.ispman.models
{

  public class AuthenticatedUser
  {
    public static var ALIAS : String='org.ufsoft.ispman.models.AuthenticatedUser';
    public var username   : String;
    public var password   : String;
    public var loginType  : int;
    public var locale     : String;

    //public var loginTypeName : Array={1 : 'Administrator', 2 : 'Reseller', 3 : 'Client', 4 : 'Domain'};

    public function AuthenticatedUser(
      username : String,
      password : String,
      loginType : int,
      locale: String)
    {
      this.username  = username;
      this.password  = password;
      this.loginType = loginType;
      this.locale    = locale;
    }

    public function getTypeName(loginType : int) : String
    {
      //return loginTypeName[loginType];
      return '';
    }
  }

}


