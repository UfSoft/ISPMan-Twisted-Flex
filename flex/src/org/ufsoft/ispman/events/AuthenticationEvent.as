/**
 * @author vampas
 */
package org.ufsoft.ispman.events {
  import flash.events.Event;
  import org.ufsoft.ispman.models.AuthenticatedUser;

  public class AuthenticationEvent extends Event {
    public static const SEND    :String = "SendAuthentication";
    public static const NEEDED  :String = "SendAuthentication";
    public static const SUCESS  :String = "AuthenticationSucessful";
    public static const FAILURE :String = "AuthenticationFailure";
    public var user             :AuthenticatedUser;

    public function AuthenticationEvent(
      type      :String,
      user      :AuthenticatedUser=null,
      bubbles   :Boolean = true,
      cancelable:Boolean = false
      )
    {
      super(type, true, cancelable);
      this.user = user;
    }

    override public function clone():Event {
      return new AuthenticationEvent( type, user, bubbles, cancelable );
    }
  }

}


