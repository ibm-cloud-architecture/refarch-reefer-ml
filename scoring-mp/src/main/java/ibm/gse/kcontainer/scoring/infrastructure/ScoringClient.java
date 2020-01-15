package ibm.gse.kcontainer.scoring.infrastructure;

import static javax.ws.rs.core.MediaType.APPLICATION_JSON;

import java.io.StringReader;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;

import javax.inject.Inject;
import javax.json.Json;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;
import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.Response;

import org.eclipse.microprofile.config.inject.ConfigProperty;

import com.google.gson.Gson;

import ibm.gse.kcontainer.scoring.domain.Telemetry;

/**
 * Call remote predictive scoring deploy on CP for data via WML.
 * Use JAX RS client code to stay dependant to other library
 */
public class ScoringClient {


    private Client client;
    // authentication token to be use to contact remote web service
    private String mlToken = null;
    @Inject
    @ConfigProperty(name = "cp4d_base_url")
    private String endPointURL;
    @Inject
    @ConfigProperty(name = "cp4d_prediction_url")
    private String predictionURL;
    @Inject
    @ConfigProperty(name = "cp4d_user")
    private String username;
    @Inject
    @ConfigProperty(name = "cp4d_pwd")
    private String password;
    
    // connection is over TLS
    private SSLContext sslcontext;
    // marshalizing from json
    static Gson parser = new Gson();

    
    public ScoringClient() {
        initSSL();
    }

    public ScoringClient(String url,String username, String pwd) {
        this.endPointURL = url;
        this.username = username;
        this.password = pwd;
        initSSL();
    }

    private void initSSL() {
        try {
            sslcontext = SSLContext.getInstance("TLS");
            sslcontext.init(null, new TrustManager[]{new X509TrustManager() {
                public void checkClientTrusted(X509Certificate[] arg0, String arg1) throws CertificateException {}
                public void checkServerTrusted(X509Certificate[] arg0, String arg1) throws CertificateException {}
                public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
            }}, new java.security.SecureRandom());
           
            client = ClientBuilder.newBuilder()
            		.sslContext(this.sslcontext)
            		.hostnameVerifier((s1,s2) -> true)
                .build();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public void close(){
        this.client.close();
    }

    public String getIAMToken() {
        String token = null;
        Response resAuth = null;
        try {
            final WebTarget targetAuth = client.target(endPointURL + "/v1/preauth/validateAuth");
            
            resAuth = targetAuth.request().header("username", username).header("password", password).get();
            System.out.println(resAuth.getStatus());
            JsonReader reader = Json.createReader(new StringReader(resAuth.readEntity(String.class)));
            JsonObject ibmAMResponse = reader.readObject();
           
            token = ibmAMResponse.getString("accessToken");
            resAuth.close();
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (resAuth != null) {
                resAuth.close();
            }
        }
        System.out.println("Token = " + token);
        return token;
    }

	public ScoringResult callAnomalyScoring(Telemetry t) {
        if (mlToken == null) {
                synchronized (this) { 
                    mlToken = getIAMToken();
                }
        }
        
        WebTarget targetResource = client.target(endPointURL + predictionURL);
        ScoringTelemetry sc = new ScoringTelemetry(t);
        Entity<String> entity = Entity.json(parser.toJson(sc));
        
        Response  rep = targetResource.request().header("Content-Type", APPLICATION_JSON)
            .header("Authorization", "Bearer " + mlToken)
            .accept(APPLICATION_JSON)
            .post(entity);
        
        ScoringResult result = parser.fromJson(rep.readEntity(String.class),ScoringResult.class);
       
       return result;
    }

	public void setPredictiveURL(String pURL) {
        this.predictionURL = pURL;
	}
}