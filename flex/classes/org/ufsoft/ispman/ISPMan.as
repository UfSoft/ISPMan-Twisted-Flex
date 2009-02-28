/**
 * @author vampas
 */
package org.ufsoft.ispman
{

  import mx.collections.ArrayCollection;

  import flash.display.DisplayObject;
  import flash.events.Event;
  import mx.containers.Canvas;
  import mx.containers.HDividedBox;
  import mx.containers.VDividedBox;
  import mx.controls.Alert;
  import mx.controls.Button;
  import mx.controls.ComboBox;
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
  import org.ufsoft.ispman.models.AuthenticatedUser;
  import org.ufsoft.ispman.events.AuthenticationEvent;

  // Modules Management
  import mx.modules.ModuleLoader;
  import mx.modules.ModuleManager;
  import mx.modules.IModuleInfo;
  import mx.events.ModuleEvent;

  // Class Alias
  import flash.net.registerClassAlias;


  public class ISPMan extends Application
  {

    [Bindable]
    public var log : String='';
    private var logger : ILogger;
    private var authDialog : Auth;
    private var user : AuthenticatedUser;


    public var mainWindow : VDividedBox;
    public var mainBox : HDividedBox;
    public var foo : Button;
    public var foo1 : Button;
    public var foo2 : Button;
    public var logout : Button;
    public var chooseDomain : ComboBox;
    public var overviewButton : Button

    // Modules
    public var overviewModule : IModuleInfo;
    public var overviewModule1 : IModuleInfo;

    public var mainWinModuleLoader : ModuleLoader;

    public function ISPMan()
    {
      super(); // Start Application
      //initLogging();
      //logger.log(LogEventLevel.INFO, "Starting application");
      // These mappings must use the same aliases defined with the PyAMF
      // function 'pyamf.register_class'.
      registerClassAlias(AuthenticatedUser.ALIAS, AuthenticatedUser);
      addEventListener(FlexEvent.CREATION_COMPLETE, creationComplete);
      addEventListener(AuthenticationEvent.NEEDED, AuthenticationNeeded);
    }

    private function initLogging() : void
    {
      // Create a target.
      var logTarget : TraceTarget=new TraceTarget();

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

    private function creationComplete(event : FlexEvent) : void
    {
      this.addEventListener(AuthenticationEvent.SUCESS, loadOverview);
      overviewButton.addEventListener("click", loadOverview);
      dispatchEvent(new AuthenticationEvent(AuthenticationEvent.NEEDED));
      //foo.addEventListener("click", fooc);
      //foo.addEventListener("click", loadModules);
      foo1.addEventListener("click", fooc1);
      foo2.addEventListener("click", fooc);
      logout.enabled = false;
      mainWinModuleLoader = new ModuleLoader();
      chooseDomain.selectedIndex = -1;
    }


    private function AuthenticationNeeded(event : Event) : void
    {
      authDialog = new AuthDLG();
      authDialog.addEventListener(AuthenticationEvent.SEND, authenticate);
      PopUpManager.addPopUp(authDialog, DisplayObject(this), true);
    }

    protected function authenticate(event : AuthenticationEvent) : void
    {
      this.user = event.user;
      var remoteObj : RemoteObject=getService();
      var operation : AbstractOperation=remoteObj.getOperation('auth.login');
      operation.addEventListener(FaultEvent.FAULT, authenticateFailure);
      operation.addEventListener(ResultEvent.RESULT, authenticateSuccess);
      operation.send(event.user);
    }

    protected function authenticateFailure(event : FaultEvent) : void
    {
      dispatchEvent(new AuthenticationEvent(AuthenticationEvent.FAILURE));
      var errorMsg : String="Authentication Failed " + event.fault.faultCode;
      Alert.show(event.fault.faultDetail, errorMsg);
    }

    protected function authenticateSuccess(event : ResultEvent) : void
    {
      this.dispatchEvent(new AuthenticationEvent(AuthenticationEvent.SUCESS));
      logout.addEventListener("click", doLogout);
      logout.enabled = true;
      PopUpManager.removePopUp(authDialog);
      log += event.result.toString() + '\n';
    }

    protected function doLogout(event : Event) : void
    {
      var remoteObj : RemoteObject=getService();
      var operation : AbstractOperation=remoteObj.getOperation('auth.logout');
      operation.addEventListener(ResultEvent.RESULT, doLogoutSucess);
      operation.addEventListener(FaultEvent.FAULT, onServiceFault);
      operation.send();
    }

    protected function doLogoutSucess(event : ResultEvent) : void
    {
      dispatchEvent(new AuthenticationEvent(AuthenticationEvent.NEEDED));
      logout.enabled = false;
    }

    private function loadModule(ml : ModuleLoader, url : String) : void
    {
      if (!ml.url)
      {
        ml.url = url;
        return ;
      }
      ml.addEventListener(ModuleEvent.READY, moduleLoaded);
      ml.addEventListener(ModuleEvent.ERROR, moduleLoadedError);
      ml.loadModule()
    }

    public function unloadModule(ml : ModuleLoader) : void
    {
      if (!ml.url)
      {
        return ;
      }
      ml.unloadModule();
    }

    private function loadModules1(event : Event=null) : void
    {
      Alert.show("Trying to load modules 1");
      overviewModule1 = ModuleManager.getModule('https://lgl:8443/module/overview2.swf');
      overviewModule1.addEventListener(ModuleEvent.READY, moduleLoaded);
      overviewModule1.addEventListener(ModuleEvent.ERROR, moduleLoadedError);
      overviewModule1.load()
      Alert.show("Trying to load modules 1- Ended;");
    }

    private function moduleLoaded(event : ModuleEvent) : void
    {
      mainWindow.addChild(event.module.factory.create()as DisplayObject);
      Alert.show("Module should be inserted by now");
    }

    private function moduleLoadedError(event : ModuleEvent) : void
    {
      Alert.show("Error loading module.");
      log += event.toString() + '\n';
    }

    protected function fooc(event : Event) : void
    {
      unloadModule(mainWinModuleLoader);
      loadModule(mainWinModuleLoader, 'https://lgl:8443/module/overview2.swf');
    }

    protected function fooc1(event : Event) : void
    {
      unloadModule(mainWinModuleLoader);
      loadModule(mainWinModuleLoader, 'https://lgl:8443/module/overview.swf');
    }

    protected function insertDefaultData_resultHandler(event : ResultEvent) : void
    {
      event.target.removeEventListener(ResultEvent.RESULT, insertDefaultData_resultHandler);
      log += event.result.toString() + '\n';
    }

    private function getService() : RemoteObject
    {
      var url : String='https://{server.name}:8443/service';
      var channel : SecureAMFChannel=new SecureAMFChannel("pyamf-channel", url);
      // Create a channel set and add your channel(s) to it
      var channels : ChannelSet=new ChannelSet();
      channels.addChannel(channel);

      // Create a new remote object and set channels
      var remoteObject : RemoteObject=new RemoteObject("ISPManService");

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
    protected function onServiceFault(event : FaultEvent) : void
    {
      if (event.fault.faultCode == 'AuthenticationNeeded')
      {
        dispatchEvent(new Event("AuthenticationNeeded", true));
      }
      else
      {
        //var errorMsg:String = 'Service error: ' + event.fault.faultCode;
        var errorMsg : String=event.fault.faultCode;
        Alert.show(event.fault.faultDetail, errorMsg);
      }
    }

    protected function getAvailableDomains() : void
    {

    }

    protected function loadOverview(event : Event) : void
    {
      loadModule(mainWinModuleLoader, 'https://lgl:8443/module/overview.swf');
      Alert.show("Loading Overview Module");
    //var remoteObj : RemoteObject=getService();
    //var operation : AbstractOperation=remoteObj.getOperation('auth.overview');
    //operation.addEventListener(FaultEvent.FAULT, authenticateFailure);
    //operation.addEventListener(ResultEvent.RESULT, authenticateSuccess);
    //operation.send(this.user);
    }
  }
}


