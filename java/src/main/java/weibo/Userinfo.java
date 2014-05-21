package weibo;

/**
 * Created with IntelliJ IDEA.
 * User: lgu
 * Date: 5/19/14
 * Time: 4:11 PM
 * To change this template use File | Settings | File Templates.
 */
public class Userinfo {
    /*{"uniqueid":"2476704054","userid":null,"displayname":"\u6d85\u69c3\u5bc2\u51c0","userdomain":"?wvr=5&lf=reg"}*/
    String uniqueid;
    String userid;
    String displayname;
    String userdomain;

    public String getUniqueid() {
        return uniqueid;
    }

    public void setUniqueid(String uniqueid) {
        this.uniqueid = uniqueid;
    }

    public String getUserid() {
        return userid;
    }

    public void setUserid(String userid) {
        this.userid = userid;
    }

    public String getDisplayname() {
        return displayname;
    }

    public void setDisplayname(String displayname) {
        this.displayname = displayname;
    }

    public String getUserdomain() {
        return userdomain;
    }

    public void setUserdomain(String userdomain) {
        this.userdomain = userdomain;
    }
}
