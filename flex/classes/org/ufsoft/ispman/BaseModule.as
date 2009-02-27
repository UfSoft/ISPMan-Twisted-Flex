/**
 * @author vampas
 */
package org.ufsoft.ispman {

  //import mx.Component;
  import mx.modules.Module;

  // To REmove
  import mx.controls.Alert;


  public class BaseModule extends Module {
    public var title  :String;

    public function BaseModule() {
      super()
      Alert.show("Module Base Created");
    }
  }
}


