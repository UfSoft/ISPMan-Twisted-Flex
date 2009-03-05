/**
 * @author vampas
 */
package org.ufsoft.ispman.events {
  import flash.events.Event;

  public class LoadDataEvent extends Event {
    public static const LOAD    :String = "LoadData";
    public static const SUCESS  :String = "LoadDataSucessful";
    public static const FAILURE :String = "LoadDataFailure";
    public var endpoint         :String;
    public var args             :Array  = new Array();

    public function LoadDataEvent(
      type      :String,
      endpoint  :String = null,
      args      :Array = null,
      bubbles   :Boolean = true,
      cancelable:Boolean = false
      )
    {
      super(type, bubbles, cancelable);
      this.endpoint = endpoint;
      this.args = args;
    }

    override public function clone():Event {
      return new LoadDataEvent( type, endpoint, args, bubbles, cancelable );
    }

    override public function toString():String {
      return formatToString("LoadDataEvent", "type", "endpoint", "args", "bubbles", "cancelable", "eventPhase");
    }
  }

}


