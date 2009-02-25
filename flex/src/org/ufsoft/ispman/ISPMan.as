/**
 * @author vampas
 */
package org.ufsoft.ispman {

  import mx.collections.ArrayCollection;

  import flash.display.DisplayObject;
  import flash.events.Event;
  import mx.controls.Alert;
  import mx.controls.Button;
  import mx.core.Application;
  import mx.events.FlexEvent;
  import mx.managers.PopUpManager;

  import mx.messaging.ChannelSet;
  import mx.messaging.channels.SecureAMFChannel;
  import mx.resources.ResourceBundle;
  import mx.rpc.AbstractOperation;
  import mx.rpc.events.FaultEvent;
  import mx.rpc.events.ResultEvent;
  import mx.rpc.remoting.mxml.RemoteObject;

  import mx.logging.targets.*;
  import mx.logging.*;


  import org.ufsoft.ispman.AuthDLG;
  import org.ufsoft.ispman.events.AuthenticationEvent;


  public class ISPMan extends Application {


    [Bindable]
    public var log        : String='';
    private var logger    : ILogger;


    private var authDialog: Auth

    private var token     : String='';

    public var foo        : Button;
    public var logout     : Button;

    [Event(name="AuthenticationNeeded", type="flash.events.Event")]

    public function ISPMan() {
      initLogging();
      logger.log(LogEventLevel.INFO, "Starting application");
      super(); // Start Application
      addEventListener( FlexEvent.CREATION_COMPLETE, creationComplete );
      addEventListener( "AuthenticationNeeded", AuthenticationNeeded );
    }

    private function initLogging():void {
      // Create a target.
      var logTarget:TraceTarget = new TraceTarget();

      // Log only messages for the classes in the mx.rpc.* and
      // mx.messaging packages.
      logTarget.filters=[]; //"mx.rpc.*","mx.messaging.*"];

      // Log all log levels.
      logTarget.level = LogEventLevel.ALL;

      // Add date, time, category, and log level to the output.
      logTarget.includeDate = true;
      logTarget.includeTime = true;
      logTarget.includeCategory = true;
      logTarget.includeLevel = true;

      // Begin logging.
      Log.addTarget(logTarget);
      logger = Log.getLogger("ISPMan");
    }


    private function AuthenticationNeeded(event:Event):void {
      authDialog = new AuthDLG();
      authDialog.addEventListener(AuthenticationEvent.SEND, authenticate);
      PopUpManager.addPopUp(authDialog, DisplayObject(this), true);
    }


    private function creationComplete(event:FlexEvent):void {
      dispatchEvent(new Event("AuthenticationNeeded", true));
      foo.addEventListener("click", fooc);
      logout.addEventListener("click", logoutc);
    }

    protected function fooc(event:Event):void {
      var remoteObj:RemoteObject = getService();
      var operation:AbstractOperation = remoteObj.getOperation('timer.time');
      operation.addEventListener(ResultEvent.RESULT, insertDefaultData_resultHandler);
      operation.send();
    }

    protected function logoutc(event:Event):void {
      var remoteObj:RemoteObject = getService();
      var operation:AbstractOperation = remoteObj.getOperation('auth.logout');
      operation.addEventListener(ResultEvent.RESULT, insertDefaultData_resultHandler);
      operation.send();
    }

    protected function insertDefaultData_resultHandler(event:ResultEvent):void {
      event.target.removeEventListener(ResultEvent.RESULT, insertDefaultData_resultHandler);
      log += event.result.toString() + '\n';
    }

    private function getService():RemoteObject {
      var url    :String = 'https://{server.name}:8443/service';
      var channel:SecureAMFChannel = new SecureAMFChannel("pyamf-channel", url);
      // Create a channel set and add your channel(s) to it
      var channels:ChannelSet = new ChannelSet();
      channels.addChannel(channel);

      // Create a new remote object and set channels
      var remoteObject:RemoteObject = new RemoteObject("ISPManService");

      remoteObject.showBusyCursor = true;
      remoteObject.channelSet = channels;
      remoteObject.addEventListener(FaultEvent.FAULT, onServiceFault);

      return remoteObject;
    }

    /**
     * Service reported an error.
     *
     * @param event Event containing error information.
     */
    protected function onServiceFault(event:FaultEvent):void {
      if ( event.fault.faultCode == 'AuthenticationNeeded') {
        dispatchEvent(new Event("AuthenticationNeeded", true));
      } else {
        //var errorMsg:String = 'Service error: ' + event.fault.faultCode;
        var errorMsg:String = event.fault.faultCode;
        Alert.show(event.fault.faultDetail, errorMsg);
      }
    }

    protected function authenticate(event:AuthenticationEvent):void {
      var remoteObj:RemoteObject = getService();
      var operation:AbstractOperation = remoteObj.getOperation('auth.login');
      operation.addEventListener(FaultEvent.FAULT, authenticateFailure);
      operation.addEventListener(ResultEvent.RESULT, authenticateSuccess);
      operation.send(event.username, event.password, event.loginType);
    }

    protected function authenticateFailure (event:FaultEvent):void {
      Alert.show("Authentication Failed ");
      trace(event);
    }

    protected function authenticateSuccess (event:ResultEvent):void {
      PopUpManager.removePopUp(authDialog);
      log += event.result.toString() + '\n';
    }
  }
}


