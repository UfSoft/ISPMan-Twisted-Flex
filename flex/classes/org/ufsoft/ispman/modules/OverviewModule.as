/**
 * @author vampas
 */
package org.ufsoft.ispman.modules {
  import org.ufsoft.ispman.BaseModule;
  //import mx.modules.Module

  import mx.controls.Alert;


  public class OverviewModule extends BaseModule {
    public function OverviewModule() {
      super();
      this.percentWidth = 100;
      this.percentHeight = 100;
      Alert.show("Overview Module Loaded");
    }
  }

}


