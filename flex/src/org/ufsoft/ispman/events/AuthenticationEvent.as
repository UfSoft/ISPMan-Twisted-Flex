/**
 * @author vampas
 */
package org.ufsoft.ispman.events {
  import flash.events.Event;

  public class AuthenticationEvent extends Event {
    public static const SEND    :String = "SendAuthentication";
    public static const SUCESS  :String = "AuthenticationSucessful";
    public static const FAILURE :String = "AuthenticationFailure";
    public var username         :String;
    public var password         :String;
    public var loginType        :int;

    public function AuthenticationEvent(
      type      :String,
      username  :String,
      password  :String,
      loginType :int,
      bubbles   :Boolean = true,
      cancelable:Boolean = false
      )
    {
      super(type, true, cancelable);
      this.username = username;
      this.password = password;
      this.loginType = loginType
    }

    override public function clone():Event {
      return new AuthenticationEvent( type, username, password, loginType, bubbles, cancelable );
    }
  }

}


