/**
 * @author vampas
 */
package org.ufsoft.ispman.models {
  public class DomainUser {

    public var uid                   : Array;
    public var givenName             : String;
    public var sn                    : String;
    public var cn                    : String;
    public var ispmanUserID          : String;
    public var mailLocalAddress      : String;
    private var userPassword         : String;
    public var mailForwardingAddress : Array;
    public var FTPStatus             : String;
    public var FTPQuotaMBytes        : int;
    public var mailQuota             : int;
    public var ispmanCreateTimestamp : int;
    public var mailAlias             : Array;

    public function DomainUser() {

    }

    public function getUID():String {
      return this.uid[0];
    }

    public function getDate():String {
      var date:Date = new Date(this.ispmanCreateTimestamp*1000);
      return date.toString();
    }
  }

}


