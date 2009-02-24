/**
 * @author vampas
 */
package org.ufsoft.ispman {

  import flash.events.Event;
  import flash.events.KeyboardEvent;
  import mx.events.FlexEvent;
  import mx.core.IFlexDisplayObject;
  import mx.events.CloseEvent;
  import mx.managers.PopUpManager;
  import mx.controls.Alert;
  import mx.containers.TitleWindow;
  import mx.events.FlexEvent;
  import mx.controls.Button;
  import mx.controls.TextInput;
  import mx.controls.ComboBox;
  import flash.events.MouseEvent;

  import org.ufsoft.ispman.events.AuthenticationEvent;
  import mx.collections.ArrayCollection;

  public class Auth extends TitleWindow {

    public var username   : TextInput;
    public var password   : TextInput;
    public var authButton : Button;
    public var loginTypeCombo: ComboBox;
    public var loginType  : int=1;
    [Bindable]
    public var loginTypeArray:ArrayCollection = new ArrayCollection([
      {label: 'Administrator', type: 1},
      {label: 'Reseller', type: 2},
      {label: 'Client', type: 3},
      ]);


    public function Auth() {
      super();
      addEventListener( FlexEvent.CREATION_COMPLETE, creationCompleteHandler );
    }

    protected function creationCompleteHandler( event:FlexEvent ):void {
      event.target.isPopUp = false; // Non movable login window
      PopUpManager.centerPopUp(this); // center the popup

      // Listen to key events to enable or not the authenticate button
      this.addEventListener(KeyboardEvent.KEY_UP, submit_Ok);

      // listen to login type changes
      loginTypeCombo.addEventListener("change", loginTypeSelect);

      // listen to authenticate button cliks to submit
      authButton.addEventListener( MouseEvent.CLICK, submitForm );

      // Set focus on username
      username.setFocus();
    }

    /*
     * Function to change the login type
     */
    private function loginTypeSelect(event:Event):void {
      loginType = ComboBox(event.target).selectedItem.type;
    }


    private function authWin_close(evt:CloseEvent):void {
      PopUpManager.removePopUp(evt.target as IFlexDisplayObject);
    }

    // Function to check if the authentication button should be enabled ot not
    private function submit_Ok(evt:KeyboardEvent):void {
      if ( password.text.length > 0 && username.text.length > 0) {
        authButton.enabled = true;
      } else {
        authButton.enabled = false;
      }
    }

    // Fire the submit form event
    private function submitForm(evt:MouseEvent):void {
      dispatchEvent(new AuthenticationEvent(
        AuthenticationEvent.SEND, username.text, password.text, loginType
        ));
    }
  }

}


